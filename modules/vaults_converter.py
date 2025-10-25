# modules/vaults_converter.py

from id_prefix import ensure_prefix, dc_ref, dc_az_ref, subnet_ref
from location_resolver import LocationResolver


def _normalize_dc_hint(value):
    if not isinstance(value, str):
        return None
    cleaned = value.strip()
    if not cleaned:
        return None
    if '.dc.' in cleaned:
        cleaned = cleaned.split('.dc.', 1)[1]
    elif cleaned.startswith('dc.'):
        cleaned = cleaned.split('dc.', 1)[1]
    return cleaned


def _resolve_dc_and_networks(resolver, vault_details, ecs_lookup):
    dc_candidates = []
    subnet_refs = set()
    for resource in vault_details.get('resources', []) or []:
        resource_id = resource.get('id')
        if not resource_id:
            continue
        ecs_details = ecs_lookup.get(resource_id)
        if not ecs_details:
            continue
        for subnet_id in ecs_details.get('subnets', []) or []:
            if subnet_id:
                subnet_refs.add(subnet_ref(subnet_id))
        for az_field in ('az', 'availability_zone'):
            az_value = ecs_details.get(az_field)
            if isinstance(az_value, str):
                az_name = az_value.strip()
                if az_name and resolver.is_valid_dc_name(az_name):
                    dc_candidates.append(az_name)
        resolved_dc = resolver.resolve_dc_name(ecs_details.get('DC'))
        if resolved_dc:
            dc_candidates.append(resolved_dc)
        fallback_dc = _normalize_dc_hint(ecs_details.get('DC'))
        if fallback_dc and resolver.is_valid_dc_name(fallback_dc):
            dc_candidates.append(fallback_dc)

    resolved_vault_dc = resolver.resolve_dc_name(vault_details.get('DC'))
    if resolved_vault_dc:
        dc_candidates.append(resolved_vault_dc)
    fallback_vault_dc = _normalize_dc_hint(vault_details.get('DC'))
    if fallback_vault_dc and resolver.is_valid_dc_name(fallback_vault_dc):
        dc_candidates.append(fallback_vault_dc)

    unique_dc = []
    for candidate in dc_candidates:
        if candidate and candidate not in unique_dc and resolver.is_valid_dc_name(candidate):
            unique_dc.append(candidate)

    return unique_dc, sorted(subnet_refs)


def convert(source_data):
    """
    Converts Vaults data to seaf.ta.services.storage and seaf.ta.services.backup formats.
    """
    ensure_prefix(source_data=source_data)
    resolver = LocationResolver(source_data)
    vaults_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.vaults', {})
    ecss_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.ecss', {}) or {}
    ecs_lookup = {}
    for ecs_details in ecss_data.values():
        if isinstance(ecs_details, dict):
            ecs_id = ecs_details.get('id')
            if ecs_id and ecs_id not in ecs_lookup:
                ecs_lookup[ecs_id] = ecs_details
    
    converted_storages = {}
    converted_backups = {}
    
    for vault_id, vault_details in vaults_data.items():
        # 1. Create Storage entity
        storage_id = vault_id
        
        description_parts = []
        if vault_details.get('description'):
            description_parts.append(vault_details.get('description'))
        if vault_details.get('tenant'):
            description_parts.append(f"Tenant: {vault_details.get('tenant')}")
        
        # Calculate total size for storage
        total_size_gb = 0
        for resource in vault_details.get('resources', []):
            # Assuming backup_size is in bytes, convert to GB
            backup_size_bytes = resource.get('backup_size', 0)
            total_size_gb += (backup_size_bytes / (1024 * 1024 * 1024)) 

        dc_names, network_refs = _resolve_dc_and_networks(resolver, vault_details, ecs_lookup)
        dc_refs = [dc_ref(dc_name) for dc_name in dc_names]
        az_refs = [dc_az_ref(dc_name) for dc_name in dc_names]

        description = '\n'.join(description_parts).strip()

        converted_storages[storage_id] = {
            'title': vault_details.get('name'),
            'description': description,
            'external_id': vault_details.get('id'),
            'type': 'Simple Storage Service', # Fixed value as per user request
            'software': 'Cloud Backup Service', # Generic for now
            'availabilityzone': az_refs,
            'location': dc_refs,
            'network_connection': network_refs,
            'sla': None, # Not available in source,
        }

        # 2. Create Backup entities for each resource
        for resource in vault_details.get('resources', []):
            if str(resource.get('protect_status', '')).lower() == 'deleted':
                continue
            backup_id = f"{vault_id}.{resource.get('id')}" # Unique ID for backup
            
            backup_description_parts = []
            if resource.get('name'):
                backup_description_parts.append(f"Resource Name: {resource.get('name')}")
            if resource.get('type'):
                backup_description_parts.append(f"Resource Type: {resource.get('type')}")
            if resource.get('size'):
                backup_description_parts.append(f"Limit Size: {resource.get('size')} GB")
            if resource.get('backup_size'):
                backup_description_parts.append(f"Current Size: {round(resource.get('backup_size') / (1024 * 1024 * 1024), 2)} GB")
            if resource.get('backup_count'):
                backup_description_parts.append(f"Backup Count: {resource.get('backup_count')}")
            if resource.get('protect_status'):
                backup_description_parts.append(f"Protect Status: {resource.get('protect_status')}")
            if resource.get('extra_info') is not None:
                backup_description_parts.append(f"Extra Info: {resource.get('extra_info')}")

            backup_description = '\n'.join(backup_description_parts).strip()

            converted_backups[backup_id] = {
                'title': f"Backup for {resource.get('name', 'Unknown')}",
                'description': backup_description,
                'external_id': resource.get('id'),
                'path': f"Vault: {vault_details.get('name')}", # Path refers to the vault
                'replication': None, # Not available in source
                'network_connection': network_refs,
                'availabilityzone': az_refs,
                'location': dc_refs,
                # Link to the storage entity
                'storage': storage_id # Reference to the created storage entity
            }

    return {
        'seaf.ta.services.storage': converted_storages,
        'seaf.ta.services.backup': converted_backups
    }
