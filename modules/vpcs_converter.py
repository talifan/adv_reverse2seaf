import ipaddress

from id_prefix import ensure_prefix, dc_ref, segment_ref
from location_resolver import LocationResolver

# modules/vpcs_converter.py

def convert(source_data):
    """
    Converts VPC data to router network devices.
    The router is linked to the predefined INT-NET segment of its primary DC.
    """
    ensure_prefix(source_data=source_data)
    resolver = LocationResolver(source_data)
    vpcs_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.vpcs', {})
    subnets_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.subnets', {})
    
    router_devices = {}

    def unique(sequence):
        seen = set()
        ordered = []
        for item in sequence:
            if item and item not in seen:
                seen.add(item)
                ordered.append(item)
        return ordered
    
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

    for vpc_id, vpc_details in vpcs_data.items():
        vpc_uuid = vpc_details.get('id')

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
        # Collect connected subnets based on CIDR inclusion
        if router_network:
            for subnet_key, subnet_network in subnet_networks.items():
                if subnet_network.subnet_of(router_network):
                    network_connections.add(subnet_key)

        dc_names = resolver.get_dc_names_for_vpc(vpc_uuid)
        if network_connections:
            for subnet_key in network_connections:
                subnet_dc = resolver.get_dc_for_subnet(subnet_key)
                if subnet_dc:
                    dc_names.append(subnet_dc)
        if not dc_names:
            fallback_dc = resolver.resolve_dc_name(vpc_details.get('DC'))
            if fallback_dc:
                dc_names.append(fallback_dc)
        dc_names = unique(dc_names)
        if any(name and not name.isdigit() for name in dc_names):
            dc_names = [name for name in dc_names if name and not name.isdigit()]

        location_refs = [dc_ref(name) for name in dc_names]

        if location_refs:
            router_description_parts.append(f"Расположение: {', '.join(location_refs)}")

        # Determine the segment reference
        int_net_segment_ref = None
        if dc_names:
            dc_name = dc_names[0]
            if dc_name:
                int_net_segment_ref = segment_ref(dc_name, 'INT-NET')

        router_id = f"{vpc_id}.router"
        router_devices[router_id] = {
            'title': f"Маршрутизатор {vpc_details.get('name') or vpc_uuid}",
            'description': '\n'.join(filter(None, router_description_parts)),
            'external_id': vpc_uuid,
            'model': 'Cloud Router',
            'realization_type': 'Виртуальный',
            'type': 'Маршрутизатор',
            'network_connection': sorted(network_connections),
            'segment': int_net_segment_ref,
            'location': location_refs
        }

    return {'seaf.ta.components.network': router_devices}
