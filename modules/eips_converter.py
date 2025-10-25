import ipaddress

from warning_reporter import collect_warning
from id_prefix import ensure_prefix, segment_ref
from location_resolver import LocationResolver


def _extract_dc_name_from_subnet(details: dict | None) -> str | None:
    if not isinstance(details, dict):
        return None
    for az_field in ('availability_zone', 'az'):
        az_value = details.get(az_field)
        if isinstance(az_value, str) and az_value.strip():
            return az_value.strip()
    dc_value = details.get('DC')
    if not isinstance(dc_value, str):
        return None
    cleaned = dc_value.strip()
    if not cleaned:
        return None
    if '.dc.' in cleaned:
        return cleaned.split('.dc.', 1)[1]
    if cleaned.startswith('dc.'):
        return cleaned.split('dc.', 1)[1]
    return cleaned


def convert(source_data):
    """
    Converts EIP data into WAN networks and network links.
    WAN networks are linked to predefined INTERNET or INT-NET segments.
    """
    ensure_prefix(source_data=source_data)
    resolver = LocationResolver(source_data)

    eips_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.eips', {})
    subnets_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.subnets', {})
    ecss_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.ecss', {})
    nat_gateways_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.nat_gateways', {})
    elbs_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.elbs', {})

    converted_networks = {}
    converted_links = {}

    # Precompute subnet networks for AZ lookup
    subnet_networks = []
    known_dc_names = set()
    for subnet_key, subnet_details in subnets_data.items():
        cidr = subnet_details.get('cidr')
        if not cidr:
            continue
        try:
            network = ipaddress.ip_network(cidr, strict=False)
        except ValueError:
            continue
        subnet_networks.append((network, subnet_details, subnet_key))
        dc_candidate = resolver.get_dc_for_subnet(subnet_key)
        if dc_candidate:
            known_dc_names.add(dc_candidate)

    fallback_dc = sorted(known_dc_names)[0] if known_dc_names else None

    # Build index from internal IP to entity references
    internal_ip_map = {}

    def register_ip(ip, reference):
        ip_norm = str(ip).strip() if ip else None
        if not ip_norm or not reference:
            return
        internal_ip_map.setdefault(ip_norm, set()).add(reference)

    for ecs_id, ecs_details in ecss_data.items():
        for ip in ecs_details.get('addresses') or []:
            register_ip(ip, ecs_id)

    for nat_id, nat_details in nat_gateways_data.items():
        register_ip(nat_details.get('address'), nat_id)

    for elb_id, elb_details in elbs_data.items():
        register_ip(elb_details.get('address'), elb_id)

    def get_dc_from_ip(ip_addr):
        if not ip_addr:
            return None
        try:
            ip_obj = ipaddress.ip_address(ip_addr)
        except ValueError:
            collect_warning(ip_addr, 'int_address', f"Invalid IP address '{ip_addr}'.")
            return None

        for network, subnet_details, subnet_key in subnet_networks:
            if ip_obj in network:
                dc_name = resolver.get_dc_for_subnet(subnet_key) or _extract_dc_name_from_subnet(subnet_details)
                if dc_name:
                    refined = resolver.resolve_dc_name(dc_name)
                    return refined or dc_name
                resolved = resolver.resolve_dc_name(subnet_details.get('DC'))
                if resolved:
                    return resolved
                return None
        return None

    for eip_key, eip_details in eips_data.items():
        description_parts = []
        if eip_details.get('int_address'):
            description_parts.append(f"Internal IP: {eip_details.get('int_address')}")
        if eip_details.get('type'):
            description_parts.append(f"Address Type: {eip_details.get('type')}")
        if eip_details.get('port_id'):
            description_parts.append(f"Port ID: {eip_details.get('port_id')}")

        limit = eip_details.get('limit', {})
        if limit:
            for key in ('rule_id', 'rule_name', 'throughput', 'type'):
                if limit.get(key):
                    description_parts.append(f"Limit {key.replace('_', ' ').title()}: {limit.get(key)}")

        if eip_details.get('tenant'):
            description_parts.append(f"Tenant: {eip_details.get('tenant')}")
        if eip_details.get('DC'):
            description_parts.append(f"DC: {eip_details.get('DC')}")

        description = '\n'.join(description_parts).strip()
        ext_ip = eip_details.get('ext_address')
        is_public = False
        if ext_ip:
            try:
                is_public = ipaddress.ip_address(ext_ip).is_global
            except ValueError:
                is_public = False

        # Determine segment based on DC of internal IP
        primary_dc = get_dc_from_ip(eip_details.get('int_address'))
        segment_list = []
        if primary_dc is None:
            primary_dc = resolver.resolve_dc_name(eip_details.get('DC'))

        if primary_dc:
            simple_dc_name = primary_dc.split('.')[-1] if '.' in primary_dc else primary_dc
            if is_public:
                segment_list.append(segment_ref(simple_dc_name, 'INTERNET'))
            else:
                segment_list.append(segment_ref(simple_dc_name, 'INT-NET'))
        elif fallback_dc:
            if is_public:
                segment_list.append(segment_ref(fallback_dc, 'INTERNET'))
            else:
                segment_list.append(segment_ref(fallback_dc, 'INT-NET'))
        else:
            collect_warning(eip_key, 'segment', "Could not determine DC for EIP, segment field will be empty.")

        converted_networks[eip_key] = {
            'title': ext_ip,
            'description': description,
            'external_id': eip_details.get('id'),
            'type': 'WAN',
            'wan_ip': ext_ip,
            'segment': segment_list,
            'provider': 'Cloud.ru'
        }

        int_ip_norm = str(eip_details.get('int_address')).strip() if eip_details.get('int_address') else None
        linked_refs = sorted(internal_ip_map.get(int_ip_norm, []))
        if linked_refs:
            link_id = f"{eip_key}.link"
            converted_links[link_id] = {
                'title': f"Связь EIP {ext_ip or eip_key}",
                'description': f"EIP {ext_ip or eip_key} связан с: {', '.join(linked_refs)}",
                'external_id': f"{eip_details.get('id')}-link" if eip_details.get('id') else link_id,
                'network_connection': [eip_key, *linked_refs],
                'technology': 'EIP'
            }

    result = {
        'seaf.ta.services.network': converted_networks
    }
    if converted_links:
        result['seaf.ta.services.network_links'] = converted_links
    return result
