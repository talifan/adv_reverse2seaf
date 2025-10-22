# modules/eips_converter.py
import ipaddress

from warning_reporter import collect_warning  # For reporting anomalies

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
    cces_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.cces', {})
    rdss_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.rdss', {})
    dmss_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.dmss', {})
    nat_gateways_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.nat_gateways', {})
    elbs_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.elbs', {})
    
    converted_networks = {}
    converted_segments = {}
    converted_links = {}
    internet_segments = {}
    known_dc_refs = set()
    
    # Build reverse index: internal IP -> set of entity references
    internal_ip_map = {}
    ecs_ip_location_map = {}

    subnets_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.subnets', {})

    # Precompute subnet networks for reuse
    subnet_networks = []
    
    def register_known_dc_from_az(az_name):
        if isinstance(az_name, str) and len(az_name) > 2:
            known_dc_refs.add(f"flix.dc.{az_name}")
    
    def register_known_dc_from_ref(dc_ref):
        if not isinstance(dc_ref, str) or not dc_ref.startswith('flix.dc.'):
            return
        suffix = dc_ref.split('flix.dc.', 1)[1]
        if suffix and len(suffix) > 2 and any(ch.isalpha() for ch in suffix) and ('-' in suffix or '.' in suffix):
            known_dc_refs.add(dc_ref)
    
    for subnet_details in subnets_data.values():
        cidr = subnet_details.get('cidr')
        if not cidr:
            continue
        try:
            subnet_networks.append((ipaddress.ip_network(cidr, strict=False), subnet_details))
        except ValueError:
            continue

    def gather_dc_refs_from_subnet(details):
        dc_refs = set()
        az = details.get('availability_zone') or details.get('az')
        if isinstance(az, str) and len(az) > 2:
            dc_ref = f"flix.dc.{az}"
            dc_refs.add(dc_ref)
            register_known_dc_from_ref(dc_ref)
        dc_field = details.get('DC')
        if isinstance(dc_field, str) and dc_field.startswith('flix.dc.'):
            dc_refs.add(dc_field)
            register_known_dc_from_ref(dc_field)
        return dc_refs

    def register_ip(ip, entity_ref):
        normalized = normalize_ip(ip)
        if not normalized or not entity_ref:
            return
        internal_ip_map.setdefault(normalized, set()).add(entity_ref)

    def register_ip_location(ip, dc_refs):
        normalized = normalize_ip(ip)
        if not normalized or not dc_refs:
            return
        ecs_ip_location_map.setdefault(normalized, set()).update(dc_refs)

    for ecs_id, ecs_details in ecss_data.items():
        addresses = ecs_details.get('addresses') or []
        ecs_dc_refs = set()
        az_name = ecs_details.get('az')
        if isinstance(az_name, str) and len(az_name) > 2:
            dc_ref = f"flix.dc.{az_name}"
            ecs_dc_refs.add(dc_ref)
            register_known_dc_from_ref(dc_ref)
        dc_field = ecs_details.get('DC')
        if isinstance(dc_field, str) and dc_field.startswith('flix.dc.'):
            ecs_dc_refs.add(dc_field)
            register_known_dc_from_ref(dc_field)
        for ip in addresses:
            register_ip(ip, ecs_id)
            register_ip_location(ip, ecs_dc_refs)

    for nat_id, nat_details in nat_gateways_data.items():
        register_ip(nat_details.get('address'), nat_id)
        register_known_dc_from_ref(nat_details.get('DC'))

    for elb_id, elb_details in elbs_data.items():
        register_ip(elb_details.get('address'), elb_id)
        az = elb_details.get('availability_zone')
        if isinstance(az, str):
            register_known_dc_from_az(az)
        dc_field = elb_details.get('DC')
        register_known_dc_from_ref(dc_field)
    for cce_details in cces_data.values():
        masters_az = cce_details.get('masters_az') or []
        if isinstance(masters_az, str):
            masters_az = [masters_az]
        for az in masters_az:
            register_known_dc_from_az(az)
        register_known_dc_from_ref(cce_details.get('DC'))
    for rds_details in rdss_data.values():
        for node in rds_details.get('nodes', []) or []:
            register_known_dc_from_az(node.get('availability_zone'))
        register_known_dc_from_ref(rds_details.get('DC'))
    for dms_details in dmss_data.values():
        available_az = dms_details.get('available_az') or []
        if isinstance(available_az, str):
            available_az = [available_az]
        for az in available_az:
            register_known_dc_from_az(az)
        register_known_dc_from_ref(dms_details.get('DC'))
    
    def ensure_internet_segment(dc_ref):
        if dc_ref not in known_dc_refs:
            return None
        az_part = dc_ref.split('flix.dc.', 1)[1]
        suffix = f"dc_{az_part.replace('-', '_')}"
        segment_id = f"flix.network_segment.internet.{suffix}"
        external_id = f"internet_segment_{suffix}"
        sber = {
            'zone': 'INTERNET',
            'location': dc_ref
        }
        if segment_id not in internet_segments:
            converted_segments[segment_id] = {
                'title': 'Public Internet',
                'description': f"Internet segment for {dc_ref}",
                'external_id': external_id,
                'sber': sber
            }
            internet_segments[segment_id] = True
        return segment_id

    for dc_ref in sorted(known_dc_refs):
        ensure_internet_segment(dc_ref)

    def find_segment_and_dcs(ip_addr):
        segment = None
        dc_refs = set()
        normalized = normalize_ip(ip_addr)
        if not normalized:
            return segment, dc_refs
        try:
            ip_to_check = ipaddress.ip_address(normalized)
        except ValueError:
            collect_warning(normalized, 'int_address', f"Invalid IP address '{ip_addr}'.")
            return segment, dc_refs

        for network, subnet_details in subnet_networks:
            if ip_to_check in network:
                vpc_id = subnet_details.get('vpc')
                if vpc_id:
                    segment = f"flix.vpcs.{vpc_id}"
                dc_refs.update(gather_dc_refs_from_subnet(subnet_details))

        dc_refs.update(ecs_ip_location_map.get(normalized, set()))
        return segment, dc_refs

    eip_records = []

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

        # Check if ext_address is public and override segment if so
        ext_address = eip_details.get('ext_address')
        is_public = False
        if ext_address:
            try:
                is_public = ipaddress.ip_address(ext_address).is_global
            except ValueError:
                is_public = False
        
        # Default segment resolution from internal IP and gather location hints
        segment_ref, derived_dc_refs = find_segment_and_dcs(eip_details.get('int_address'))

        dc_refs = set(derived_dc_refs)
        dc_field = eip_details.get('DC')
        if isinstance(dc_field, str) and dc_field.startswith('flix.dc.'):
            dc_refs.add(dc_field)
            register_known_dc_from_ref(dc_field)

        filtered_dc_refs = sorted([dc for dc in dc_refs if dc in known_dc_refs])

        if dc_refs and not filtered_dc_refs:
            collect_warning(eip_id, 'DC', "Unable to map referenced data centers to known AZ-derived DCs. Skipping location binding.")

        location_refs = filtered_dc_refs

        converted_networks[new_id] = {
            'title': eip_details.get('ext_address'),
            'description': description,
            'external_id': eip_details.get('id'),
            'type': 'WAN',
            'wan_ip': ext_address,
            'segment': [],
            'provider': 'Cloud.ru'
        }
        eip_records.append({
            'id': new_id,
            'is_public': is_public,
            'segment_ref': segment_ref,
            'dc_refs': filtered_dc_refs,
            'data': converted_networks[new_id]
        })

        if is_public:
            if not filtered_dc_refs:
                # Ensure at least a global segment exists
                ensure_internet_segment(None)
            for dc in (filtered_dc_refs or [None]):
                ensure_internet_segment(dc)

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

    # Finalize segment references for each EIP network
    for record in eip_records:
        if record['is_public']:
            if not internet_segments:
                collect_warning(record['id'], 'segment', "No Internet segments available to attach. Check DC configuration.")
                record['data']['segment'] = []
            else:
                record['data']['segment'] = sorted(internet_segments.keys())
        else:
            segment = record['segment_ref']
            if segment:
                record['data']['segment'] = [segment]
            else:
                record['data']['segment'] = []

    # The main converter script handles merging entities of the same type,
    # so we can return both dictionaries.
    result = {
        'seaf.ta.services.network': converted_networks,
        'seaf.ta.services.network_segment': converted_segments
    }
    if converted_links:
        result['seaf.ta.services.network_links'] = converted_links
    return result
