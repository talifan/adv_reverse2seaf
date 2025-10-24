# modules/peerings_converter.py

from id_prefix import ensure_prefix, build_id

def find_router_key(vpc_id):
    """Constructs the full key for a router from its VPC ID."""
    # This assumes that a router is created with an ID of '<prefix>.vpcs.<vpc_id>.router'
    return build_id('vpcs', vpc_id, 'router') if vpc_id else None

def convert(source_data):
    """
    Converts VPC Peerings data to seaf.ta.services.network_links format.
    The network link connects routers that represent the peered VPCs.
    """
    ensure_prefix(source_data=source_data)
    peerings_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.peerings', {})
    
    converted_links = {}
    
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

        # Resolve endpoints to the routers of the peered VPCs
        request_vpc_id = peering_details.get('request_vpc')
        source_router_ref = find_router_key(request_vpc_id)
        
        accept_vpc_id = peering_details.get('accept_vpc')
        target_router_ref = find_router_key(accept_vpc_id)

        endpoints = [ref for ref in (source_router_ref, target_router_ref) if ref]
        if len(endpoints) < 2:
            # Skip link if we can't resolve both endpoints
            continue

        converted_links[new_id] = {
            'title': peering_details.get('name'),
            'description': description,
            'external_id': peering_details.get('id'),
            'network_connection': endpoints,
            'technology': 'VPC Peering'
        }

    if not converted_links:
        return {}

    return {'seaf.ta.services.network_links': converted_links}
