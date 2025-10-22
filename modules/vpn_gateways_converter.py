# modules/vpn_gateways_converter.py

def normalize_az(value):
    """Normalize AZ values to a list of non-empty strings."""
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

def find_network_key(source_data, subnet_id):
    """Finds the full key for a Network from its subnet ID."""
    return f"flix.subnets.{subnet_id}" if subnet_id else None

def find_network_segment_key(vpc_id):
    """Constructs the full key for a Network Segment from its VPC ID."""
    return f"flix.vpcs.{vpc_id}" if vpc_id else None

def convert(source_data):
    """
    Converts VPN Gateway data to seaf.ta.components.network format.
    """
    vpn_gateways_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.vpn_gateways', {})
    subnets_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.subnets', {})
    ecss_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.ecss', {})
    
    converted_networks = {}
    
    for vpn_gw_id, vpn_gw_details in vpn_gateways_data.items():
        new_id = vpn_gw_id
        
        description_parts = []
        if vpn_gw_details.get('ip_address'):
            description_parts.append(f"IP Address: {vpn_gw_details.get('ip_address')}")
        if vpn_gw_details.get('type'):
            description_parts.append(f"Protocol: {vpn_gw_details.get('type')}")
        if vpn_gw_details.get('tenant'):
            description_parts.append(f"Tenant: {vpn_gw_details.get('tenant')}")

        description = '\n'.join(description_parts).strip()

        # Resolve network_connection (subnet_id)
        subnet_id = vpn_gw_details.get('subnet_id')
        network_connection_refs = []
        if subnet_id:
            network_connection_refs.append(find_network_key(source_data, subnet_id))
        network_connection_refs = [ref for ref in network_connection_refs if ref] # Filter out None values

        subnet_details = subnets_data.get(f"flix.subnets.{subnet_id}") or subnets_data.get(subnet_id) or next(
            (details for key, details in subnets_data.items() if details.get('id') == subnet_id), None
        )

        # Resolve segment from vpc_id
        vpc_id = vpn_gw_details.get('vpc_id')
        segment_ref = find_network_segment_key(vpc_id)

        az_names = set()
        az_names.update(normalize_az(vpn_gw_details.get('availability_zone')))
        if subnet_details:
            az_names.update(normalize_az(subnet_details.get('availability_zone')))
            az_names.update(normalize_az(subnet_details.get('az')))

        # Inspect ECS instances to enrich AZ data
        for ecs_details in ecss_data.values():
            ecs_subnets = ecs_details.get('subnets') or []
            if subnet_id and subnet_id in ecs_subnets:
                az_names.update(normalize_az(ecs_details.get('az')))
                for disk_item in ecs_details.get('disks', []):
                    if isinstance(disk_item, dict):
                        for disk_props in disk_item.values():
                            if isinstance(disk_props, dict):
                                az_names.update(normalize_az(disk_props.get('az')))

        location_refs = sorted({f"flix.dc.{az}" for az in az_names if isinstance(az, str) and az})

        dc_hints = set()
        if subnet_details:
            subnet_dc = subnet_details.get('DC')
            if isinstance(subnet_dc, str) and subnet_dc.startswith('flix.dc.'):
                dc_hints.add(subnet_dc)
        vpn_dc_hint = vpn_gw_details.get('DC')
        if isinstance(vpn_dc_hint, str) and vpn_dc_hint.startswith('flix.dc.'):
            dc_hints.add(vpn_dc_hint)

        if not location_refs:
            location_refs = sorted(dc_hints)

        if location_refs:
            # Append location into description for traceability
            location_str = ', '.join(location_refs)
            description = (description + f"\nDC: {location_str}").strip() if description else f"DC: {location_str}"

        converted_networks[new_id] = {
            'title': vpn_gw_details.get('name'),
            'description': description,
            'external_id': vpn_gw_details.get('id'),
            'model': 'Cloud VPN Gateway', # Default value
            'realization_type': 'Виртуальный', # Fixed value for VPN Gateway
            'type': 'VPN', # Fixed value for VPN Gateway
            'network_connection': network_connection_refs,
            'segment': segment_ref,
            'location': location_refs,
            'address': vpn_gw_details.get('ip_address') # IP Address of the VPN Gateway
        }

    return {'seaf.ta.components.network': converted_networks}
