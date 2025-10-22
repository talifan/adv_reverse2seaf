# modules/nat_gateways_converter.py
import json  # For dumping rules to description

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

def find_subnet_entry(subnets_data, subnet_id):
    """Return tuple (key, details) for subnet_id if found."""
    if not subnet_id:
        return None, None
    for key, details in subnets_data.items():
        if details.get('id') == subnet_id or key == subnet_id or key.endswith(subnet_id):
            return key, details
    return None, None


def convert(source_data):
    """
    Converts NAT Gateway data to seaf.ta.components.network format.
    """
    nat_gateways_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.nat_gateways', {})
    subnets_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.subnets', {})
    ecss_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.ecss', {})
    
    converted_networks = {}
    
    for nat_id, nat_details in nat_gateways_data.items():
        new_id = nat_id
        
        description_parts = []
        if nat_details.get('description'):
            description_parts.append(nat_details.get('description'))
        if nat_details.get('address'):
            description_parts.append(f"Internal IP: {nat_details.get('address')}")
        if nat_details.get('status'):
            description_parts.append(f"Status: {nat_details.get('status')}")
        if nat_details.get('tenant'):
            description_parts.append(f"Tenant: {nat_details.get('tenant')}")
        # Add SNAT and DNAT rules to description as JSON for now
        snat_rules = nat_details.get('snat_rules', [])
        if snat_rules:
            description_parts.append(f"SNAT Rules: {json.dumps(snat_rules, indent=2)}")
        dnat_rules = nat_details.get('dnat_rules', [])
        description_parts.append(f"DNAT Rules: {json.dumps(dnat_rules, indent=2)}")

        # Resolve network_connection (subnet_id)
        subnet_id = nat_details.get('subnet_id')
        subnet_key, subnet_details = find_subnet_entry(subnets_data, subnet_id)

        network_connection_refs = []
        if subnet_id:
            network_connection_refs.append(f"flix.subnets.{subnet_id}")
        network_connection_refs = [ref for ref in network_connection_refs if ref]  # Filter out None values

        # Resolve segment from subnet_id
        segment_ref = None
        subnet_vpc_id = None
        if subnet_details:
            subnet_vpc_id = subnet_details.get('vpc')
            if subnet_vpc_id:
                segment_ref = f"flix.vpcs.{subnet_vpc_id}"

        # Resolve location based on AZ/DC data
        az_names = set()
        az_names.update(normalize_az(nat_details.get('availability_zone')))
        if subnet_details:
            az_names.update(normalize_az(subnet_details.get('availability_zone')))
            az_names.update(normalize_az(subnet_details.get('az')))

        # Look for ECS instances that reside in the same subnet
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
        nat_dc_hint = nat_details.get('DC')
        if isinstance(nat_dc_hint, str) and nat_dc_hint.startswith('flix.dc.'):
            dc_hints.add(nat_dc_hint)

        if not location_refs:
            location_refs = sorted(dc_hints)

        if location_refs:
            description_parts.append(f"DC: {', '.join(location_refs)}")
        elif nat_details.get('DC'):
            description_parts.append(f"DC: {nat_details.get('DC')}")

        description = '\n'.join(description_parts).strip()

        converted_networks[new_id] = {
            'title': nat_details.get('name'),
            'description': description,
            'external_id': nat_details.get('id'),
            'model': 'Cloud NAT Gateway', # Default value
            'realization_type': 'Виртуальный', # Fixed value for NAT Gateway
            'type': 'NAT', # Fixed value for NAT Gateway
            'network_connection': network_connection_refs,
            'segment': segment_ref,
            'location': location_refs,
            'address': nat_details.get('address') # Internal IP
        }

    return {'seaf.ta.components.network': converted_networks}
