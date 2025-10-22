# modules/dmss_converter.py

from warning_reporter import collect_warning  # For collecting conversion warnings

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

        # Resolve AZ references with validation
        available_az_raw = dms_details.get('available_az')
        if available_az_raw is None:
            collect_warning(dms_id, 'available_az', "Missing 'available_az'. Location will be empty.")
            available_az_iter = []
        elif isinstance(available_az_raw, str):
            available_az_iter = [available_az_raw]
        elif isinstance(available_az_raw, (list, tuple, set)):
            available_az_iter = list(available_az_raw)
        else:
            collect_warning(dms_id, 'available_az', f"Invalid type '{type(available_az_raw).__name__}' for 'available_az'. Expected string or list.")
            available_az_iter = []

        valid_available_az = []
        for az_name in available_az_iter:
            if isinstance(az_name, str) and len(az_name) > 2:
                valid_available_az.append(az_name)
            else:
                collect_warning(f"{dms_id}.available_az", 'value', f"Invalid AZ value '{az_name}'. Skipping.")

        if available_az_iter and not valid_available_az:
            collect_warning(dms_id, 'available_az', "No valid AZ values found. Location will be empty.")

        az_refs = [find_dc_az_key(source_data, az_name) for az_name in valid_available_az]
        az_refs = [ref for ref in az_refs if ref] # Filter out None values

        # Resolve location (DC) based on available_az
        location_refs = [f"flix.dc.{az_name}" for az_name in valid_available_az if az_name]
        location_refs = [ref for ref in location_refs if ref] # Filter out None values

        # Resolve network_connection (subnet_id)
        network_connection_refs = []
        subnet_id = dms_details.get('subnet_id')
        if not subnet_id:
            collect_warning(dms_id, 'subnet_id', "Missing or empty 'subnet_id'. network_connection will be empty.")
        elif not isinstance(subnet_id, str):
            collect_warning(dms_id, 'subnet_id', f"Invalid type '{type(subnet_id).__name__}' for 'subnet_id'. network_connection will be empty.")
            subnet_id = None
        if subnet_id:
            network_connection_refs.append(find_network_key(source_data, subnet_id))
        network_connection_refs = [ref for ref in network_connection_refs if ref] # Filter out None values

        if not dms_details.get('vpc_id'):
            collect_warning(dms_id, 'vpc_id', "Missing 'vpc_id'. Ensure upstream segment references are available.")

        converted_clusters[new_id] = {
            'title': dms_details.get('name'),
            'description': description,
            'external_id': dms_details.get('id'),
            'fqdn': dms_details.get('address'),
            'reservation_type': dms_details.get('type'),
            'service_type': 'Интеграционная шина  (MQ, ETL, API)', # Fixed value for DMS
            'availabilityzone': az_refs,
            'location': location_refs,
            'network_connection': network_connection_refs,
        }

    return {'seaf.ta.services.cluster': converted_clusters}
