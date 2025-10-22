# modules/subnets_converter.py

def find_vpc_key(source_data, vpc_id):
    """Finds the full key for a VPC from its ID."""
    vpcs_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.vpcs', {})
    for key, details in vpcs_data.items():
        if details.get('id') == vpc_id:
            return key
    return None

def convert(source_data):
    """
    Converts Subnet data to seaf.ta.services.network format.
    """
    subnets_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.subnets', {})
    
    converted_networks = {}
    
    for subnet_id, subnet_details in subnets_data.items():
        new_id = subnet_id
        
        description = subnet_details.get('description', '')
        if subnet_details.get('gateway'):
            description += f"\nGateway: {subnet_details.get('gateway')}"
        if subnet_details.get('dns_list'):
            dns_list_str = ', '.join(subnet_details.get('dns_list', []))
            description += f"\nDNS: {dns_list_str}"
        if subnet_details.get('tenant'):
            description += f"\nTenant: {subnet_details.get('tenant')}"
        
        # Find the corresponding network_segment key.
        vpc_key = find_vpc_key(source_data, subnet_details.get('vpc'))
        
        # Determine network type based on name
        network_type = 'LAN'
        if 'WAN' in subnet_details.get('name', '').upper():
            network_type = 'WAN'

        converted_networks[new_id] = {
            'title': subnet_details.get('name'),
            'description': description.strip(),
            'external_id': subnet_details.get('id'),
            'type': network_type,
            'ipnetwork': subnet_details.get('cidr'),
            'segment': [vpc_key] if vpc_key else []
        }

        # Add provider for WAN networks or lan_type for LAN networks
        if network_type == 'WAN':
            converted_networks[new_id]['provider'] = 'Cloud.ru'
        elif network_type == 'LAN':
            converted_networks[new_id]['lan_type'] = 'Проводная'

    return {'seaf.ta.services.network': converted_networks}
