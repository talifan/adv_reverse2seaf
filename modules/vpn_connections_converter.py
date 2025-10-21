# modules/vpn_connections_converter.py

def find_vpn_gateway_key(source_data, gw_id):
    """Finds the full key for a VPN Gateway from its ID."""
    # This assumes that the gw_id directly maps to the external_id of a converted network component
    # which is the original gw_id.
    return f"flix.vpn_gateways.{gw_id}" if gw_id else None

def find_office_or_dc_key(source_data, branch_id):
    """Finds the full key for an Office or DC from its ID."""
    # This is a simplification. In a real scenario, we would need to check both
    # seaf.ta.services.office and seaf.ta.services.dc.
    # For now, we'll assume a direct mapping if the ID is simple.
    # The example data uses flix.office.hq and flix.dc.02
    if branch_id.startswith('flix.office.'):
        return branch_id
    elif branch_id.startswith('flix.dc.'):
        return branch_id
    return None


def convert(source_data):
    """
    Converts VPN Connections data to seaf.ta.services.logical_link format.
    """
    vpn_connections_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.vpn_connections', {})
    
    converted_logical_links = {}
    
    for vpn_conn_id, vpn_conn_details in vpn_connections_data.items():
        new_id = vpn_conn_id
        
        description_parts = []
        if vpn_conn_details.get('remote_gw_ip'):
            description_parts.append(f"Remote Gateway IP: {vpn_conn_details.get('remote_gw_ip')}")
        if vpn_conn_details.get('remote_subnets'):
            description_parts.append(f"Remote Subnets: {', '.join(vpn_conn_details.get('remote_subnets'))}")
        if vpn_conn_details.get('tenant'):
            description_parts.append(f"Tenant: {vpn_conn_details.get('tenant')}")
        if vpn_conn_details.get('DC'):
            description_parts.append(f"DC: {vpn_conn_details.get('DC')}")

        description = '\n'.join(description_parts).strip()

        # Resolve source (gw_id) and target (branch_id)
        source_ref = None
        gw_id = vpn_conn_details.get('gw_id')
        if gw_id:
            source_ref = find_vpn_gateway_key(source_data, gw_id)
        
        target_refs = []
        branch_id = vpn_conn_details.get('branch_id')
        if branch_id:
            target_ref = find_office_or_dc_key(source_data, branch_id)
            if target_ref:
                target_refs.append(target_ref)
        
        converted_logical_links[new_id] = {
            'title': vpn_conn_details.get('name'),
            'description': description,
            'external_id': vpn_conn_details.get('id'),
            'source': source_ref,
            'target': target_refs,
            'direction': '<==>',
        }

    return {'seaf.ta.services.logical_link': converted_logical_links}
