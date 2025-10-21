# modules/vaults_converter.py

def convert(source_data):
    """
    Converts Vaults data to seaf.ta.services.storage and seaf.ta.services.backup formats.
    """
    vaults_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.vaults', {})
    
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

        description = '\n'.join(description_parts).strip()

        converted_storages[storage_id] = {
            'title': vault_details.get('name'),
            'description': description,
            'external_id': vault_details.get('id'),
            'type': 'Simple Storage Service', # Fixed value as per user request
            'software': 'Cloud Backup Service', # Generic for now
            'availabilityzone': [], # Not available in source
            'location': [vault_details.get('DC')] if vault_details.get('DC') else [],
            'network_connection': [], # Not available in source
            'sla': None, # Not available in source,
        }

        # 2. Create Backup entities for each resource
        for resource in vault_details.get('resources', []):
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
                'network_connection': [], # Not available in source
                'availabilityzone': [], # Not available in source
                'location': [vault_details.get('DC')] if vault_details.get('DC') else [],
                # Link to the storage entity
                'storage': storage_id # Reference to the created storage entity
            }

    return {
        'seaf.ta.services.storage': converted_storages,
        'seaf.ta.services.backup': converted_backups
    }
