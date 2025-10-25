# modules/subnets_converter.py

from id_prefix import ensure_prefix, segment_ref
from location_resolver import LocationResolver

def _normalize_dc_name(value):
    """Extract simple DC identifier from various representations."""
    if not isinstance(value, str):
        return None
    cleaned = value.strip()
    if not cleaned:
        return None
    if '.dc.' in cleaned:
        return cleaned.split('.dc.', 1)[1]
    if cleaned.startswith('dc.'):
        return cleaned.split('dc.', 1)[1]
    return cleaned

def convert(source_data):
    """
    Converts Subnet data to seaf.ta.services.network format.
    Each subnet is linked to the predefined INT-NET segment of its DC (derived from AZ).
    """
    ensure_prefix(source_data=source_data)
    resolver = LocationResolver(source_data)
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
        
        # Determine the segment reference from AZ/DC data
        dc_name = None
        for az_field in ('availability_zone', 'az'):
            az_value = subnet_details.get(az_field)
            if isinstance(az_value, str) and az_value.strip():
                dc_name = az_value.strip()
                break
        if not dc_name:
            dc_name = resolver.get_dc_for_subnet(subnet_id)
        if not dc_name:
            dc_name = resolver.resolve_dc_name(subnet_details.get('DC'))
        if not dc_name:
            normalized_dc = _normalize_dc_name(subnet_details.get('DC'))
            if normalized_dc and resolver.is_valid_dc_name(normalized_dc):
                dc_name = normalized_dc
        if not dc_name:
            vpc_id = subnet_details.get('vpc')
            if vpc_id:
                vpc_dc_candidates = resolver.get_dc_names_for_vpc(vpc_id)
                if vpc_dc_candidates:
                    dc_name = vpc_dc_candidates[0]
        if dc_name and not resolver.is_valid_dc_name(dc_name):
            dc_name = None

        int_net_segment_ref = segment_ref(dc_name, 'INT-NET') if dc_name else None
        
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
            'segment': [int_net_segment_ref] if int_net_segment_ref else []
        }

        # Add provider for WAN networks or lan_type for LAN networks
        if network_type == 'WAN':
            converted_networks[new_id]['provider'] = 'Cloud.ru'
        elif network_type == 'LAN':
            converted_networks[new_id]['lan_type'] = 'Проводная'

    return {'seaf.ta.services.network': converted_networks}
