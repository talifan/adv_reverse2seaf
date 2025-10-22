# modules/eips_converter.py
import ipaddress

def normalize_ip(ip):
    """Return stripped IP string or None."""
    if not ip:
        return None
    ip = str(ip).strip()
    return ip or None

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
    Converts EIPs (Elastic IP addresses) data to seaf.ta.services.network format (WAN type)
    and creates a single network_segment for all public-facing EIPs. Additionally, it builds
    network links that reflect bindings between the WAN network and internal resources
    (servers, NAT-шлюзы, балансировщики).
    """
    eips_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.eips', {})
    ecss_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.ecss', {})
    nat_gateways_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.nat_gateways', {})
    elbs_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.elbs', {})
    
    converted_networks = {}
    converted_segments = {}
    converted_links = {}
    
    # Build reverse index: internal IP -> set of entity references
    internal_ip_map = {}

    def register_ip(ip, entity_ref):
        normalized = normalize_ip(ip)
        if not normalized or not entity_ref:
            return
        internal_ip_map.setdefault(normalized, set()).add(entity_ref)

    for ecs_id, ecs_details in ecss_data.items():
        addresses = ecs_details.get('addresses') or []
        for ip in addresses:
            register_ip(ip, ecs_id)

    for nat_id, nat_details in nat_gateways_data.items():
        register_ip(nat_details.get('address'), nat_id)

    for elb_id, elb_details in elbs_data.items():
        register_ip(elb_details.get('address'), elb_id)
    
    has_public_eips = False

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

        # Default segment resolution from internal IP
        segment_ref = find_segment_from_ip(source_data, eip_details.get('int_address'))

        # Check if ext_address is public and override segment if so
        ext_address = eip_details.get('ext_address')
        is_public = False
        if ext_address:
            try:
                is_public = ipaddress.ip_address(ext_address).is_global
            except ValueError:
                is_public = False
        
        if is_public:
            segment_ref = "flix.network_segment.internet"
            has_public_eips = True

        converted_networks[new_id] = {
            'title': eip_details.get('ext_address'),
            'description': description,
            'external_id': eip_details.get('id'),
            'type': 'WAN',
            'wan_ip': ext_address,
            'segment': segment_ref,
            'location': [eip_details.get('DC')] if eip_details.get('DC') else [],
            'provider': 'Cloud.ru'
        }

        # Build network link if we can resolve internal associations
        int_ip_normalized = normalize_ip(eip_details.get('int_address'))
        linked_entities = sorted(internal_ip_map.get(int_ip_normalized, []))
        if linked_entities:
            network_connection = [new_id] + linked_entities
            link_description_parts = [
                f"EIP {eip_details.get('ext_address') or new_id} связан с: {', '.join(linked_entities)}"
            ]
            link_id = f"{new_id}.link"
            converted_links[link_id] = {
                'title': f"Связь EIP {eip_details.get('ext_address') or new_id}",
                'description': '\n'.join(link_description_parts),
                'external_id': f"{eip_details.get('id')}-link" if eip_details.get('id') else link_id,
                'network_connection': network_connection,
                'technology': 'EIP'
            }

    # Create the single "Internet" segment if any public EIPs were found
    if has_public_eips:
        converted_segments['flix.network_segment.internet'] = {
            'title': 'Public Internet',
            'description': 'Logical segment for all public-facing IP addresses.',
            'external_id': 'internet_segment',
            'sber': {
                'zone': 'INTERNET'
            }
        }

    # The main converter script handles merging entities of the same type,
    # so we can return both dictionaries.
    result = {
        'seaf.ta.services.network': converted_networks,
        'seaf.ta.services.network_segment': converted_segments
    }
    if converted_links:
        result['seaf.ta.services.network_links'] = converted_links
    return result
