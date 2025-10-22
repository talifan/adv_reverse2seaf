import ipaddress

# modules/vpcs_converter.py

def convert(source_data):
    """
    Converts VPC data to the target flix.vpcs format.
    """
    vpcs_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.vpcs', {})
    subnets_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.subnets', {})
    ecss_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.ecss', {})
    cces_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.cces', {})
    rdss_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.rdss', {})
    dmss_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.dmss', {})
    
    converted_vpcs = {}
    router_devices = {}
    
    # Pre-calculate subnet CIDRs for fast lookup when building router connections
    subnet_networks = {}
    for subnet_key, subnet_details in subnets_data.items():
        cidr = subnet_details.get('cidr')
        if not cidr:
            continue
        try:
            subnet_networks[subnet_key] = ipaddress.ip_network(cidr, strict=False)
        except ValueError:
            continue

    def normalize_az(value):
        if not value:
            return []
        if isinstance(value, str):
            value = value.strip()
            return [value] if value else []
        if isinstance(value, (list, tuple, set)):
            result = []
            for item in value:
                if isinstance(item, str):
                    item = item.strip()
                    if item:
                        result.append(item)
            return result
        return []
    
    for vpc_id, vpc_details in vpcs_data.items():
        new_id = vpc_id
        vpc_uuid = vpc_details.get('id')

        description_parts = []
        if vpc_details.get('description'):  # Include original description
            description_parts.append(vpc_details.get('description'))
        if vpc_details.get('cidr'):
            description_parts.append(f"CIDR: {vpc_details.get('cidr')}")
        if vpc_details.get('tenant'):
            description_parts.append(f"Tenant: {vpc_details.get('tenant')}")
        description = '\n'.join(description_parts)

        router_description_parts = [
            f"Связанная VPC: {vpc_details.get('name') or vpc_uuid}",
            f"CIDR: {vpc_details.get('cidr')}"
        ]

        router_network = None
        vpc_cidr = vpc_details.get('cidr')
        if vpc_cidr:
            try:
                router_network = ipaddress.ip_network(vpc_cidr, strict=False)
            except ValueError:
                router_description_parts.append("Внимание: некорректный CIDR VPC")

        network_connections = set()
        az_names = set()
        dc_hints = set()

        # Collect connected subnets based on CIDR inclusion
        if router_network:
            for subnet_key, subnet_network in subnet_networks.items():
                if subnet_network.subnet_of(router_network):
                    network_connections.add(subnet_key)
                    subnet_details = subnets_data.get(subnet_key, {})
                    az_names.update(normalize_az(subnet_details.get('availability_zone')))
                    az_names.update(normalize_az(subnet_details.get('az')))
                    dc_hint = subnet_details.get('DC')
                    if isinstance(dc_hint, str) and dc_hint:
                        dc_hints.add(dc_hint)

        # Collect AZs/DCs from ECS
        for ecs_details in ecss_data.values():
            if ecs_details.get('vpc_id') == vpc_uuid:
                az_names.update(normalize_az(ecs_details.get('az')))
                for disk_item in ecs_details.get('disks', []):
                    if isinstance(disk_item, dict):
                        for disk_props in disk_item.values():
                            if isinstance(disk_props, dict):
                                az_names.update(normalize_az(disk_props.get('az')))
                dc_hint = ecs_details.get('DC')
                if isinstance(dc_hint, str) and dc_hint:
                    dc_hints.add(dc_hint)

        # Collect AZs from CCE clusters
        for cce_details in cces_data.values():
            if cce_details.get('vpc_id') == vpc_uuid:
                az_names.update(normalize_az(cce_details.get('masters_az')))
                az_names.update(normalize_az(cce_details.get('workers_az')))

        # Collect AZs/DCs from RDS instances
        for rds_details in rdss_data.values():
            if rds_details.get('vpc_id') == vpc_uuid:
                az_names.update(normalize_az(rds_details.get('az')))
                dc_hint = rds_details.get('DC')
                if isinstance(dc_hint, str) and dc_hint:
                    dc_hints.add(dc_hint)

        # Collect AZs/DCs from DMS services
        for dms_details in dmss_data.values():
            if dms_details.get('vpc_id') == vpc_uuid:
                az_names.update(normalize_az(dms_details.get('available_az')))
                dc_hint = dms_details.get('DC')
                if isinstance(dc_hint, str) and dc_hint:
                    dc_hints.add(dc_hint)

        location_refs = sorted({f"flix.dc.{az}" for az in az_names if isinstance(az, str) and az})
        if not location_refs:
            location_refs = sorted({hint for hint in dc_hints if hint.startswith('flix.dc.')})
        if not location_refs:
            fallback_dc = vpc_details.get('DC')
            if isinstance(fallback_dc, str) and fallback_dc.startswith('flix.dc.'):
                location_refs = [fallback_dc]

        if location_refs:
            router_description_parts.append(f"Расположение: {', '.join(location_refs)}")

        converted_vpcs[new_id] = {
            'title': vpc_details.get('name'),
            'description': description,
            'external_id': vpc_uuid,
            'sber': {
                'location': location_refs[0] if location_refs else vpc_details.get('DC', ''),
                'zone': '###PLACEHOLDER_FOR_MANUAL_ZONE###'
            }
        }

        router_id = f"{vpc_id}.router"
        router_devices[router_id] = {
            'title': f"Маршрутизатор {vpc_details.get('name') or vpc_uuid}",
            'description': '\n'.join(filter(None, router_description_parts)),
            'external_id': vpc_uuid,
            'model': 'Cloud Router',
            'realization_type': 'Виртуальный',
            'type': 'Маршрутизатор',
            'network_connection': sorted(network_connections),
            'segment': new_id,
            'location': location_refs
        }

    converted_data = {'seaf.ta.services.network_segment': converted_vpcs}
    converted_data['seaf.ta.components.network'] = router_devices
    return converted_data
