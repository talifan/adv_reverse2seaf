# modules/eips_converter.py
import ipaddress

def find_segment_from_ip(source_data, ip_addr):
    """Finds the network segment by checking which subnet's CIDR contains the IP."""
    if not ip_addr:
        return None
    
    try:
        ip_to_check = ipaddress.ip_address(ip_addr)
    except ValueError:
        return None # Invalid IP address

    subnets_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.subnets', {})
    for subnet_key, subnet_details in subnets_data.items():
        cidr = subnet_details.get('cidr')
        if cidr:
            try:
                net = ipaddress.ip_network(cidr)
                if ip_to_check in net:
                    vpc_id = subnet_details.get('vpc')
                    if vpc_id:
                        return f"flix.vpcs.{vpc_id}"
            except ValueError:
                continue # Ignore invalid CIDRs
    return None

def convert(source_data):
    """
    Converts EIPs (Elastic IP addresses) data to seaf.ta.services.network format (WAN type).
    """
    eips_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.eips', {})
    
    converted_networks = {}
    
    for eip_id, eip_details in eips_data.items():
        new_id = eip_id
        
        description_parts = []
        if eip_details.get('int_address'):
            description_parts.append(f"Internal IP: {eip_details.get('int_address')}")
        if eip_details.get('type'):
            description_parts.append(f"Address Type: {eip_details.get('type')}")
        if eip_details.get('port_id'):
            description_parts.append(f"Port ID: {eip_details.get('port_id')}")
        
        limit_details = eip_details.get('limit', {})
        if limit_details:
            if limit_details.get('rule_id'):
                description_parts.append(f"Limit Rule ID: {limit_details.get('rule_id')}")
            if limit_details.get('rule_name'):
                description_parts.append(f"Limit Rule Name: {limit_details.get('rule_name')}")
            if limit_details.get('throughput'):
                description_parts.append(f"Limit Throughput (Mbps): {limit_details.get('throughput')}")
            if limit_details.get('type'):
                description_parts.append(f"Limit Type: {limit_details.get('type')}")
        
        if eip_details.get('tenant'):
            description_parts.append(f"Tenant: {eip_details.get('tenant')}")
        if eip_details.get('DC'):
            description_parts.append(f"DC: {eip_details.get('DC')}")

        description = '\n'.join(description_parts).strip()

        # Resolve segment from internal IP address
        segment_ref = find_segment_from_ip(source_data, eip_details.get('int_address'))

        converted_networks[new_id] = {
            'title': eip_details.get('ext_address'),
            'description': description,
            'external_id': eip_details.get('id'),
            'type': 'WAN', # Fixed value for EIP
            'wan_ip': eip_details.get('ext_address'), # Map external address to wan_ip
            'segment': segment_ref,
            'location': [eip_details.get('DC')] if eip_details.get('DC') else [],
            'provider': 'Cloud.ru'
            # Other fields like segment, etc. are not available in source or set to None
        }

    return {'seaf.ta.services.network': converted_networks}
