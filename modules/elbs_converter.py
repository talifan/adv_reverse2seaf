# modules/elbs_converter.py
import json  # For dumping listeners and pools to description

from id_prefix import ensure_prefix, subnet_ref, dc_ref, dc_az_ref
from location_resolver import LocationResolver
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
    Converts ELB (Elastic Load Balancer) data to seaf.ta.components.network format.
    """
    ensure_prefix(source_data=source_data)
    resolver = LocationResolver(source_data)
    elbs_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.elbs', {})
    subnets_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.subnets', {})
    ecss_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.ecss', {})
    
    converted_services = {}

    def unique(sequence):
        seen = set()
        ordered = []
        for item in sequence:
            if item and item not in seen:
                seen.add(item)
                ordered.append(item)
        return ordered
    
    for elb_id, elb_details in elbs_data.items():
        new_id = elb_id
        
        description_parts = []
        if elb_details.get('description'):
            description_parts.append(elb_details.get('description'))
        if elb_details.get('address'):
            description_parts.append(f"Internal IP: {elb_details.get('address')}")
        if elb_details.get('operating_status'):
            description_parts.append(f"Operating Status: {elb_details.get('operating_status')}")
        if elb_details.get('provisioning_status'):
            description_parts.append(f"Provisioning Status: {elb_details.get('provisioning_status')}")
        if elb_details.get('tags'):
            tags_str = ', '.join([f"{tag['key']}:{tag['value']}" for tag in elb_details.get('tags')])
            description_parts.append(f"Tags: {tags_str}")
        if elb_details.get('tenant'):
            description_parts.append(f"Tenant: {elb_details.get('tenant')}")
        # Add listeners and pools to description as JSON for now
        listeners = elb_details.get('listeners', [])
        if listeners:
            description_parts.append(f"Listeners: {json.dumps(listeners, indent=2)}")
        pools = elb_details.get('pools', [])
        if pools:
            description_parts.append(f"Pools: {json.dumps(pools, indent=2)}")

        # Resolve network_connection (subnet_id)
        subnet_id = elb_details.get('subnet_id')
        subnet_key, subnet_details_found = find_subnet_entry(subnets_data, subnet_id)

        network_connection_refs = []
        if subnet_id:
            network_connection_refs.append(subnet_ref(subnet_id))
        network_connection_refs = [ref for ref in network_connection_refs if ref]  # Filter out None values

        # Resolve location and segment based on AZ/DC data
        az_names = set()
        az_names.update(normalize_az(elb_details.get('availability_zone')))
        if subnet_details_found:
            az_names.update(normalize_az(subnet_details_found.get('availability_zone')))
            az_names.update(normalize_az(subnet_details_found.get('az')))

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

        dc_candidates = []
        if subnet_id:
            subnet_dc = resolver.get_dc_for_subnet(subnet_id)
            if subnet_dc:
                dc_candidates.append(subnet_dc)
        for az_name in az_names:
            resolved = resolver.resolve_dc_name(az_name)
            if resolved:
                dc_candidates.append(resolved)
        if subnet_details_found:
            subnet_dc_hint = resolver.resolve_dc_name(subnet_details_found.get('DC'))
            if subnet_dc_hint:
                dc_candidates.append(subnet_dc_hint)
        elb_dc_hint = resolver.resolve_dc_name(elb_details.get('DC'))
        if elb_dc_hint:
            dc_candidates.append(elb_dc_hint)

        dc_names = unique(dc_candidates)
        if any(name and not name.isdigit() for name in dc_names):
            dc_names = [name for name in dc_names if name and not name.isdigit()]
        location_refs = [dc_ref(name) for name in dc_names]

        if location_refs:
            description_parts.append(f"DC: {', '.join(location_refs)}")
        elif elb_details.get('DC'):
            description_parts.append(f"DC: {elb_details.get('DC')}")

        primary_dc_name = dc_names[0] if dc_names else None
        az_refs = [dc_az_ref(name) for name in az_names if isinstance(name, str) and name]

        description = '\n'.join(description_parts).strip()

        converted_services[new_id] = {
            'title': elb_details.get('name'),
            'description': description,
            'external_id': elb_details.get('id'),
            'service_type': 'Шлюз, Балансировщик, прокси',
            'availabilityzone': az_refs if az_refs else ([dc_az_ref(primary_dc_name)] if primary_dc_name else []),
            'network_connection': network_connection_refs,
            'location': location_refs
        }

    return {'seaf.ta.services.compute_service': converted_services}
