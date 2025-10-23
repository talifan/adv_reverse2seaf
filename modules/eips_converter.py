import ipaddress

from warning_reporter import collect_warning
from id_prefix import (
    ensure_prefix,
    build_id,
    vpc_ref,
    dc_ref,
    subnet_ref,
    get_prefix,
)


def _add_dc_from_az(target: set[str], az_value):
    if isinstance(az_value, str) and az_value.strip():
        target.add(dc_ref(az_value.strip()))
    elif isinstance(az_value, (list, tuple, set)):
        for item in az_value:
            _add_dc_from_az(target, item)


def _add_dc_from_field(target: set[str], dc_value):
    if not isinstance(dc_value, str) or not dc_value.strip():
        return
    value = dc_value.strip()
    prefix = get_prefix()
    if value.startswith(f"{prefix}.dc."):
        suffix = value.split(f"{prefix}.dc.", 1)[1]
        if suffix and any(ch.isalpha() for ch in suffix) and '-' in suffix:
            target.add(value)
        return
    if '-' in value and any(ch.isalpha() for ch in value):
        target.add(dc_ref(value))


def _build_internet_segment(dc_reference: str) -> tuple[str, dict]:
    prefix = get_prefix()
    if not dc_reference.startswith(f"{prefix}.dc."):
        return None, {}
    suffix = dc_reference.split(f"{prefix}.dc.", 1)[1].replace('-', '_').replace('.', '_')
    segment_id = build_id('network_segment', 'internet', suffix)
    segment_payload = {
        'title': 'Public Internet',
        'description': f"Internet segment for {dc_reference}",
        'external_id': f"internet_segment_{suffix}",
        'sber': {
            'zone': 'INTERNET',
            'location': dc_reference
        }
    }
    return segment_id, segment_payload


def _infer_vpc_reference(subnet_details):
    vpc_id = subnet_details.get('vpc')
    return vpc_ref(vpc_id) if vpc_id else None


def convert(source_data):
    """
    Converts EIP data into WAN networks, Internet segments per data center,
    and network links that bind WAN networks to internal resources.
    """
    ensure_prefix(source_data=source_data)

    eips_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.eips', {})
    subnets_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.subnets', {})
    ecss_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.ecss', {})
    nat_gateways_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.nat_gateways', {})
    elbs_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.elbs', {})
    cces_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.cces', {})
    rdss_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.rdss', {})
    dmss_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.dmss', {})

    converted_networks = {}
    converted_segments = {}
    converted_links = {}

    known_dc_refs = set()

    # Collect DC references from various entities
    for subnet_details in subnets_data.values():
        _add_dc_from_az(known_dc_refs, subnet_details.get('availability_zone') or subnet_details.get('az'))
        _add_dc_from_field(known_dc_refs, subnet_details.get('DC'))

    for ecs_details in ecss_data.values():
        _add_dc_from_az(known_dc_refs, ecs_details.get('az'))
        _add_dc_from_field(known_dc_refs, ecs_details.get('DC'))
        for disk_item in ecs_details.get('disks', []):
            if isinstance(disk_item, dict):
                for disk_props in disk_item.values():
                    if isinstance(disk_props, dict):
                        _add_dc_from_az(known_dc_refs, disk_props.get('az'))

    for cce_details in cces_data.values():
        _add_dc_from_az(known_dc_refs, cce_details.get('masters_az'))
        _add_dc_from_az(known_dc_refs, cce_details.get('workers_az'))
        _add_dc_from_field(known_dc_refs, cce_details.get('DC'))

    for rds_details in rdss_data.values():
        _add_dc_from_az(known_dc_refs, rds_details.get('az'))
        for node in rds_details.get('nodes', []) or []:
            if isinstance(node, dict):
                _add_dc_from_az(known_dc_refs, node.get('availability_zone'))
        _add_dc_from_field(known_dc_refs, rds_details.get('DC'))

    for dms_details in dmss_data.values():
        _add_dc_from_az(known_dc_refs, dms_details.get('available_az'))
        _add_dc_from_field(known_dc_refs, dms_details.get('DC'))

    for nat_details in nat_gateways_data.values():
        _add_dc_from_field(known_dc_refs, nat_details.get('DC'))

    for elb_details in elbs_data.values():
        _add_dc_from_az(known_dc_refs, elb_details.get('availability_zone'))
        _add_dc_from_field(known_dc_refs, elb_details.get('DC'))

    # Precompute subnet networks for segment lookup
    subnet_networks = []
    for subnet_details in subnets_data.values():
        cidr = subnet_details.get('cidr')
        if not cidr:
            continue
        try:
            network = ipaddress.ip_network(cidr, strict=False)
        except ValueError:
            continue
        subnet_networks.append((network, subnet_details))

    # Build index from internal IP to entity references
    internal_ip_map = {}

    def register_ip(ip, reference):
        ip_norm = str(ip).strip() if ip else None
        if not ip_norm or not reference:
            return
        internal_ip_map.setdefault(ip_norm, set()).add(reference)

    for ecs_id in ecss_data.keys():
        ecs_details = ecss_data[ecs_id]
        for ip in ecs_details.get('addresses') or []:
            register_ip(ip, ecs_id)

    for nat_id, nat_details in nat_gateways_data.items():
        register_ip(nat_details.get('address'), nat_id)

    for elb_id, elb_details in elbs_data.items():
        register_ip(elb_details.get('address'), elb_id)

    # Generate Internet segments per known data center
    internet_segment_ids = []
    for dc_reference in sorted(known_dc_refs):
        segment_id, payload = _build_internet_segment(dc_reference)
        if segment_id and segment_id not in converted_segments:
            converted_segments[segment_id] = payload
            internet_segment_ids.append(segment_id)

    def resolve_segment_from_ip(ip_addr):
        if not ip_addr:
            return None
        try:
            ip_obj = ipaddress.ip_address(ip_addr)
        except ValueError:
            collect_warning(ip_addr, 'int_address', f"Invalid IP address '{ip_addr}'.")
            return None

        for network, subnet_details in subnet_networks:
            if ip_obj in network:
                return _infer_vpc_reference(subnet_details)
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

        private_segment = resolve_segment_from_ip(eip_details.get('int_address'))

        converted_networks[eip_key] = {
            'title': ext_ip,
            'description': description,
            'external_id': eip_details.get('id'),
            'type': 'WAN',
            'wan_ip': ext_ip,
            'segment': [],
            'provider': 'Cloud.ru'
        }

        if is_public:
            if internet_segment_ids:
                converted_networks[eip_key]['segment'] = list(internet_segment_ids)
            else:
                collect_warning(eip_key, 'segment', "No Internet segments could be created; segment field left empty.")
        else:
            if private_segment:
                converted_networks[eip_key]['segment'] = [private_segment]
            else:
                converted_networks[eip_key]['segment'] = []

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
        'seaf.ta.services.network': converted_networks,
        'seaf.ta.services.network_segment': converted_segments
    }
    if converted_links:
        result['seaf.ta.services.network_links'] = converted_links
    return result
