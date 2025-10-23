# modules/vpn_connections_converter.py

from id_prefix import ensure_prefix, build_id
def normalize_reference(identifier, default_type):
    if not identifier or not isinstance(identifier, str):
        return None
    identifier = identifier.strip()
    if '.' in identifier:
        return identifier
    return build_id(default_type, identifier)


def find_vpn_gateway_key(source_data, gw_id):
    """Finds the full key for a VPN Gateway from its ID."""
    return normalize_reference(gw_id, 'vpn_gateways')

def find_office_or_dc_key(source_data, branch_id):
    """Finds the full key for an Office or DC from its ID."""
    normalized = normalize_reference(branch_id, 'office')
    if normalized and '.dc.' in normalized:
        return normalized
    if normalized:
        return normalized
    return None


def convert(source_data):
    """
    Converts VPN Connections data to seaf.ta.services.logical_link format.
    """
    ensure_prefix(source_data=source_data)
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
