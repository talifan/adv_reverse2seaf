# modules/peerings_converter.py

from id_prefix import ensure_prefix, vpc_ref


def find_network_segment_key(source_data, vpc_id):
    """Finds the full key for a Network Segment from its VPC ID."""
    # This assumes that the vpc_id directly maps to the external_id of a converted network_segment
    # which is the original vpc_id.
    # So, if a vpc with id 'd48e294f-eb6a-4352-8d73-275b7a966e90' was converted to '<prefix>.vpcs.d48e294f-eb6a-4352-8d73-275b7a966e90'
    # then we can construct the key.
    return vpc_ref(vpc_id) if vpc_id else None

def convert(source_data):
    """
    Converts VPC Peerings data to seaf.ta.services.logical_link format.
    """
    ensure_prefix(source_data=source_data)
    peerings_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.peerings', {})
    
    converted_logical_links = {}
    
    for peering_id, peering_details in peerings_data.items():
        new_id = peering_id
        
        description_parts = []
        if peering_details.get('description'):
            description_parts.append(peering_details.get('description'))
        if peering_details.get('status'):
            description_parts.append(f"Status: {peering_details.get('status')}")
        if peering_details.get('tenant'):
            description_parts.append(f"Tenant: {peering_details.get('tenant')}")
        if peering_details.get('DC'):
            description_parts.append(f"DC: {peering_details.get('DC')}")

        description = '\n'.join(description_parts).strip()

        # Resolve endpoints (request_vpc and accept_vpc)
        endpoints_refs = []
        request_vpc_id = peering_details.get('request_vpc')
        if request_vpc_id:
            endpoints_refs.append(find_network_segment_key(source_data, request_vpc_id))
        
        accept_vpc_id = peering_details.get('accept_vpc')
        if accept_vpc_id:
            endpoints_refs.append(find_network_segment_key(source_data, accept_vpc_id))
        
        endpoints_refs = [ref for ref in endpoints_refs if ref] # Filter out None values

        # Ensure we have at least two endpoints for a peering
        source_endpoint = endpoints_refs[0] if len(endpoints_refs) > 0 else None
        target_endpoint = [endpoints_refs[1]] if len(endpoints_refs) > 1 else []

        converted_logical_links[new_id] = {
            'title': peering_details.get('name'),
            'description': description,
            'external_id': peering_details.get('id'),
            'source': source_endpoint,
            'target': target_endpoint,
            'direction': '<==>',
        }

    return {'seaf.ta.services.logical_link': converted_logical_links}
