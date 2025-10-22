# modules/vpn_gateways_converter.py

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
        if vpn_gw_details.get('DC'):
            description_parts.append(f"DC: {vpn_gw_details.get('DC')}")

        description = '\n'.join(description_parts).strip()

        # Resolve network_connection (subnet_id)
        subnet_id = vpn_gw_details.get('subnet_id')
        network_connection_refs = []
        if subnet_id:
            network_connection_refs.append(find_network_key(source_data, subnet_id))
        network_connection_refs = [ref for ref in network_connection_refs if ref] # Filter out None values

        # Resolve segment from vpc_id
        vpc_id = vpn_gw_details.get('vpc_id')
        segment_ref = find_network_segment_key(vpc_id)

        converted_networks[new_id] = {
            'title': vpn_gw_details.get('name'),
            'description': description,
            'external_id': vpn_gw_details.get('id'),
            'model': 'Cloud VPN Gateway', # Default value
            'realization_type': 'Виртуальный', # Fixed value for VPN Gateway
            'type': 'VPN', # Fixed value for VPN Gateway
            'network_connection': network_connection_refs,
            'segment': segment_ref,
            'location': [vpn_gw_details.get('DC')] if vpn_gw_details.get('DC') else [],
            'address': vpn_gw_details.get('ip_address') # IP Address of the VPN Gateway
        }

    return {'seaf.ta.components.network': converted_networks}
