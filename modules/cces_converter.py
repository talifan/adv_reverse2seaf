# modules/cces_converter.py

from warning_reporter import collect_warning  # For collecting conversion warnings
from id_prefix import get_prefix, build_id

def find_dc_az_key(source_data, az_name):
    """Finds the full key for a DC AZ from its name."""
    return build_id("dc_az", az_name) if az_name else None

def find_network_key(source_data, subnet_id):
    """Finds the full key for a Network from its subnet ID."""
    return build_id("subnets", subnet_id) if subnet_id else None

def find_kb_key(source_data, auth_type, tag):
    """Finds or constructs a key for a KB entity based on authentication type and tag."""
    # This is a simplification. In a real scenario, we might need to create the KB entity
    # if it doesn't exist, or have a more complex lookup.
    # For now, we'll construct a key based on the auth_type and tag.
    return build_id("kb", f"{tag.lower()}", f"{auth_type.lower()}") if auth_type and tag else None


def convert(source_data):
    """
    Converts CCE (Cloud Container Engine) data to seaf.ta.services.k8s format.
    """
    cces_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.cces', {})
    
    converted_k8s_clusters = {}
    
    for cce_id, cce_details in cces_data.items():
        new_id = cce_id
        
        description_parts = []
        if cce_details.get('flavor'):
            description_parts.append(f"Flavor: {cce_details.get('flavor')}")
        if cce_details.get('platform_version'):
            description_parts.append(f"Platform Version: {cce_details.get('platform_version')}")
        if cce_details.get('addresses'):
            description_parts.append(f"IP Addresses: {', '.join(cce_details.get('addresses'))}")
        if cce_details.get('security_groups'):
            description_parts.append(f"Security Groups: {', '.join(cce_details.get('security_groups'))}")
        if cce_details.get('container_network'):
            description_parts.append(f"Container Network: {cce_details.get('container_network')}")
        if cce_details.get('tenant'):
            description_parts.append(f"Tenant: {cce_details.get('tenant')}")
        
        # Alias is mapped to description as per mapping_analysis.md
        if cce_details.get('alias'):
            description_parts.append(f"Alias: {cce_details.get('alias')}")

        description = '\n'.join(description_parts).strip()

        # Resolve AZ references with validation
        masters_az_raw = cce_details.get('masters_az')
        masters_az_values = []
        if masters_az_raw is None:
            collect_warning(cce_id, 'masters_az', "Missing 'masters_az'. Location will be empty.")
            masters_az_iterable = []
        elif isinstance(masters_az_raw, str):
            masters_az_iterable = [masters_az_raw]
        elif isinstance(masters_az_raw, (list, tuple, set)):
            masters_az_iterable = list(masters_az_raw)
        else:
            collect_warning(cce_id, 'masters_az', f"Invalid type '{type(masters_az_raw).__name__}' for 'masters_az'. Expected string or list.")
            masters_az_iterable = []

        for az_name in masters_az_iterable:
            if isinstance(az_name, str) and len(az_name) > 2:
                masters_az_values.append(az_name)
            else:
                collect_warning(f"{cce_id}.masters_az", 'value', f"Invalid AZ value '{az_name}'. Skipping.")

        if masters_az_iterable and not masters_az_values:
            collect_warning(cce_id, 'masters_az', "No valid AZ values found. Location will be empty.")

        az_refs = [find_dc_az_key(source_data, az_name) for az_name in masters_az_values]
        az_refs = [ref for ref in az_refs if ref] # Filter out None values

        # Resolve network_connection (subnet_id)
        network_connection_refs = []
        subnet_id = cce_details.get('subnet_id')
        if not subnet_id:
            collect_warning(cce_id, 'subnet_id', "Missing or empty 'subnet_id'. network_connection will be empty.")
        elif not isinstance(subnet_id, str):
            collect_warning(cce_id, 'subnet_id', f"Invalid type '{type(subnet_id).__name__}' for 'subnet_id'. network_connection will be empty.")
            subnet_id = None
        if subnet_id:
            network_connection_refs.append(find_network_key(source_data, subnet_id))
        network_connection_refs = [ref for ref in network_connection_refs if ref]

        # Resolve management_networks (service_network)
        management_network_refs = []
        service_network_cidr = cce_details.get('service_network')
        if service_network_cidr:
            # This is a simplification. Ideally, we would create a new network entity for this CIDR
            # and then link to it. For now, we'll just use the CIDR as a placeholder.
            management_network_refs.append(f"cidr.{service_network_cidr.replace('/', '_').replace('.', '_')}")
        management_network_refs = [ref for ref in management_network_refs if ref]

        # Resolve service_mesh
        service_mesh_value = "istio" if cce_details.get('supportistio') else None

        # Resolve auth (authentication)
        auth_ref = find_kb_key(source_data, cce_details.get('authentication'), "IdP") # Assuming IdP tag for authentication

        # Resolve location (DC) based on masters_az
        location_refs = [build_id("dc", az_name) for az_name in masters_az_values]
        location_refs = [ref for ref in location_refs if ref] # Filter out None values

        converted_k8s_clusters[new_id] = {
            'title': cce_details.get('name'),
            'description': description,
            'external_id': cce_details.get('id'),
            'fqdn': next((ep.get('url') for ep in cce_details.get('endpoints', []) if ep.get('type') == 'Internal'), None),
            'software': f"CCE {cce_details.get('version')}" if cce_details.get('version') else None,
            'availabilityzone': az_refs,
            'location': location_refs,
            'service_mesh': service_mesh_value,
            'network_connection': network_connection_refs,
            'management_networks': management_network_refs,
            'auth': auth_ref,
            'is_own': None, # Not available in source, set to None
            'cni': None, # Not available in source, set to None
            'cluster_autoscaler': None, # Not available in source, set to None
            'keys': None, # Not available in source, set to None
            'idm': None, # Not available in source, set to None
            'policy': None, # Not available in source, set to None
            'pam': None, # Not available in source, set to None
            'ca': None, # Not available in source, set to None
            'audit': None, # Not available in source, set to None
            'audit_policy': None, # Not available in source, set to None
            'monitoring': [], # Not available in source, set to empty list
            'backup': [], # Not available in source, set to empty list
            'registries': [], # Not available in source, set to empty list
        }

    return {'seaf.ta.services.k8s': converted_k8s_clusters}
