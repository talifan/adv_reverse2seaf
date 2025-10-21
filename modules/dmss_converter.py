# modules/dmss_converter.py

def find_dc_az_key(source_data, az_name):
    """Finds the full key for a DC AZ from its name, with robust validation."""
    if isinstance(az_name, str) and len(az_name) > 2: # Robust check for AZ name
        return f"flix.dc_az.{az_name}" # Construct reference to the specific AZ
    return None

def find_network_key(source_data, subnet_id):
    """Finds the full key for a Network from its subnet ID."""
    return f"flix.subnets.{subnet_id}" if subnet_id else None

def convert(source_data):
    """
    Converts DMS (Distributed Message Services) data to seaf.ta.services.cluster format.
    """
    dmss_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.dmss', {})
    
    converted_clusters = {}
    
    for dms_id, dms_details in dmss_data.items():
        new_id = dms_id
        
        description_parts = []
        if dms_details.get('engine'):
            description_parts.append(f"Engine: {dms_details.get('engine')}")
        if dms_details.get('engine_version'):
            description_parts.append(f"Engine Version: {dms_details.get('engine_version')}")
        if dms_details.get('port'):
            description_parts.append(f"Port: {dms_details.get('port')}")
        if dms_details.get('status'):
            description_parts.append(f"Status: {dms_details.get('status')}")
        if dms_details.get('specification'):
            description_parts.append(f"Specification: {dms_details.get('specification')}")
        if dms_details.get('security_groups'):
            description_parts.append(f"Security Groups: {', '.join(dms_details.get('security_groups'))}")
        if dms_details.get('storage_space'):
            description_parts.append(f"Storage Space: {dms_details.get('storage_space')}")
        if dms_details.get('total_storage_space'):
            description_parts.append(f"Total Storage Space: {dms_details.get('total_storage_space')}")
        if dms_details.get('used_storage_space'):
            description_parts.append(f"Used Storage Space: {dms_details.get('used_storage_space')}")
        if dms_details.get('storage_spec_code'):
            description_parts.append(f"Storage Spec Code: {dms_details.get('storage_spec_code')}")
        if dms_details.get('management'):
            description_parts.append(f"Management URL: {dms_details.get('management')}")
        if dms_details.get('support_features'):
            description_parts.append(f"Supported Features: {dms_details.get('support_features')}")
        if dms_details.get('node_num'):
            description_parts.append(f"Node Num: {dms_details.get('node_num')}")
        if dms_details.get('disk_encrypted') is not None:
            description_parts.append(f"Disk Encrypted: {dms_details.get('disk_encrypted')}")
        if dms_details.get('tenant'):
            description_parts.append(f"Tenant: {dms_details.get('tenant')}")
        if dms_details.get('DC'):
            description_parts.append(f"DC: {dms_details.get('DC')}")

        description = '\n'.join(description_parts).strip()

        # Resolve AZ references
        az_refs = [find_dc_az_key(source_data, az_name) for az_name in dms_details.get('available_az', [])]
        az_refs = [ref for ref in az_refs if ref] # Filter out None values

        # Resolve network_connection (subnet_id)
        network_connection_refs = []
        subnet_id = dms_details.get('subnet_id')
        if subnet_id:
            network_connection_refs.append(find_network_key(source_data, subnet_id))
        network_connection_refs = [ref for ref in network_connection_refs if ref] # Filter out None values

        converted_clusters[new_id] = {
            'title': dms_details.get('name'),
            'description': description,
            'external_id': dms_details.get('id'),
            'fqdn': dms_details.get('address'),
            'reservation_type': dms_details.get('type'),
            'service_type': 'Интеграционная шина  (MQ, ETL, API)', # Fixed value for DMS
            'availabilityzone': az_refs,
            'location': [dms_details.get('DC')] if dms_details.get('DC') else [],
            'network_connection': network_connection_refs,
        }

    return {'seaf.ta.services.cluster': converted_clusters}
