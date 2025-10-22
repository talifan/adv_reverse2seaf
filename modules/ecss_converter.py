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
        
        cpu_details = ecs_details.get('cpu', {})

        description_parts = []
        if ecs_details.get('description'):
            description_parts.append(ecs_details.get('description'))
        if ecs_details.get('flavor'):
            description_parts.append(f"Flavor: {ecs_details.get('flavor')}")
        if cpu_details.get('arch'):
            description_parts.append(f"CPU Architecture: {cpu_details.get('arch')}")
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

        converted_disks = []
        disks_data = ecs_details.get('disks', [])
        if isinstance(disks_data, dict):
            disks_data = [disks_data]

        for disk_item in disks_data:
            if not isinstance(disk_item, dict):
                continue

            for disk_id, disk_props in disk_item.items():
                if not isinstance(disk_props, dict):
                    continue

                size_raw = disk_props.get('size')
                size_gb = 0
                if size_raw:
                    size_str = str(size_raw).strip()
                    numeric_chars = []
                    for char in size_str:
                        if char.isdigit() or (char == '.' and '.' not in numeric_chars):
                            numeric_chars.append(char)
                        else:
                            break
                    if numeric_chars:
                        try:
                            size_gb = int(float("".join(numeric_chars)))
                        except ValueError:
                            size_gb = 0
                
                converted_disks.append({
                    'az': find_dc_az_key(source_data, disk_props.get('az')),
                    'size': size_gb,
                    'type': disk_props.get('type'),
                    'device': disk_props.get('device')
                })
        
        ram_mb = ecs_details.get('ram', 0)
        ram_gb = ram_mb // 1024 if ram_mb else 0

        az_ref = find_dc_az_key(source_data, ecs_details.get('az'))
        az_name = ecs_details.get('az')
        location_ref = [f"flix.dc.{az_name}"] if az_name else []
        subnet_refs = [find_network_key(source_data, s_id) for s_id in ecs_details.get('subnets', [])]
        subnet_refs = [ref for ref in subnet_refs if ref]

        freq_raw = cpu_details.get('frequency')
        freq_mhz = 0
        if freq_raw:
            freq_str = str(freq_raw).strip()
            numeric_chars = []
            for char in freq_str:
                if char.isdigit() or (char == '.' and '.' not in numeric_chars):
                    numeric_chars.append(char)
                else:
                    break
            if numeric_chars:
                try:
                    freq_mhz = int(float("".join(numeric_chars)))
                except ValueError:
                    freq_mhz = 0

        converted_servers[new_id] = {
            'title': ecs_details.get('name'),
            'description': description,
            'external_id': ecs_details.get('id'),
            'type': 'Виртуальный',
            'fqdn': ecs_details.get('name'),
            'os': {
                'type': ecs_details.get('os', {}).get('type'),
                'bit': ecs_details.get('os', {}).get('bit')
            },
            'cpu': {
                'cores': cpu_details.get('cores'),
                'frequency': freq_mhz
            },
            'ram': ram_gb,
            'nic_qty': ecs_details.get('nic_qty'),
            'disks': converted_disks,
            'az': [az_ref] if az_ref else [],
            'location': location_ref,
            'subnets': subnet_refs,
            'virtualization': 'flix.cluster_virtualization.cloud_ru_virtualization_cluster'
        }

    return {'seaf.ta.components.server': converted_servers}
