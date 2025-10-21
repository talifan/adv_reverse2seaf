# modules/ecss_converter.py

def find_dc_az_key(source_data, az_name):
    """Finds the full key for a DC AZ from its name."""
    # In a real scenario, we would have a mapping or a way to look up DC AZs
    # For now, we'll assume a direct mapping if the name is simple, or return None
    # based on the example data, DC AZs are like 'ru-moscow-1a'
    # and the target schema expects a reference like 'flix.dc_az.ru-moscow-1a'
    return f"flix.dc_az.{az_name}" if az_name else None

def find_network_key(source_data, subnet_id):
    """Finds the full key for a Network from its subnet ID."""
    # This assumes that the subnet_id in ecss directly maps to the external_id of a converted network
    # which is the original subnet_id.
    # So, if a subnet with id '0d9f37b6-0889-4763-8cf3-20d9641af0c1' was converted to 'flix.subnets.0d9f37b6-0889-4763-8cf3-20d9641af0c1'
    # then we can construct the key.
    return f"flix.subnets.{subnet_id}" if subnet_id else None


def convert(source_data):
    """
    Converts ECS (Elastic Cloud Server) data to seaf.ta.components.server format.
    """
    ecss_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.ecss', {})
    
    converted_servers = {}
    
    for ecs_id, ecs_details in ecss_data.items():
        new_id = ecs_id
        
        description_parts = []
        if ecs_details.get('description'):
            description_parts.append(ecs_details.get('description'))
        if ecs_details.get('flavor'):
            description_parts.append(f"Flavor: {ecs_details.get('flavor')}")
        if ecs_details.get('status'):
            description_parts.append(f"Status: {ecs_details.get('status')}")
        if ecs_details.get('addresses'):
            description_parts.append(f"IP Addresses: {', '.join(ecs_details.get('addresses'))}")
        if ecs_details.get('security_groups'):
            description_parts.append(f"Security Groups: {', '.join(ecs_details.get('security_groups'))}")
        if ecs_details.get('tags'):
            tags_str = ', '.join([f"{tag['key']}:{tag['value']}" for tag in ecs_details.get('tags')])
            description_parts.append(f"Tags: {tags_str}")
        if ecs_details.get('tenant'):
            description_parts.append(f"Tenant: {ecs_details.get('tenant')}")
        if ecs_details.get('DC'):
            description_parts.append(f"DC: {ecs_details.get('DC')}")

        description = '\n'.join(description_parts).strip()

        # Convert disks
        converted_disks = []
        # Assuming disks is a list of dictionaries, where each dictionary is a disk
        for disk_details in ecs_details.get('disks', []):
            if isinstance(disk_details, dict):
                converted_disks.append({
                    'az': find_dc_az_key(source_data, disk_details.get('az')),
                    'size': int(disk_details.get('size')) if disk_details.get('size') else 0,
                    'type': disk_details.get('type'),
                    'device': disk_details.get('device')
                })
        
        # Convert RAM from MB to GB
        ram_mb = ecs_details.get('ram', 0)
        ram_gb = ram_mb // 1024 if ram_mb else 0

        # Resolve AZ and Subnet references
        az_ref = find_dc_az_key(source_data, ecs_details.get('az'))
        subnet_refs = [find_network_key(source_data, s_id) for s_id in ecs_details.get('subnets', [])]
        subnet_refs = [ref for ref in subnet_refs if ref] # Filter out None values

        converted_servers[new_id] = {
            'title': ecs_details.get('name'),
            'description': description,
            'external_id': ecs_details.get('id'),
            'type': 'Виртуальный', # Fixed value for ECS
            'fqdn': ecs_details.get('name'), # Using name as fqdn for now
            'os': {
                'type': ecs_details.get('os', {}).get('type'),
                'bit': ecs_details.get('os', {}).get('bit')
            },
            'cpu': {
                'cores': ecs_details.get('cpu', {}).get('cores'),
                'frequency': int(ecs_details.get('cpu', {}).get('frequency')) if ecs_details.get('cpu', {}).get('frequency') else 0 # Convert to int
            },
            'ram': ram_gb,
            'nic_qty': ecs_details.get('nic_qty'),
            'disks': converted_disks,
            'az': [az_ref] if az_ref else [],
            'subnets': subnet_refs,
            'virtualization': 'flix.cluster_virtualization.cloud_ru_virtualization_cluster' # Filled with reference to virtualization cluster
            # Other fields like is_part_of_compute_service, etc. are left as None/empty for now
        }

    return {'seaf.ta.components.server': converted_servers}
