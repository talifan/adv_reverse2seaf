# modules/ecss_converter.py

from warning_reporter import collect_warning # Import for collecting warnings
from id_prefix import ensure_prefix, dc_az_ref, subnet_ref, build_id, dc_ref


def find_dc_az_key(source_data, az_name):
    """Finds the full key for a DC AZ from its name."""
    return dc_az_ref(az_name) if az_name else None

def find_network_key(source_data, subnet_id):
    """Finds the full key for a Network from its subnet ID."""
    return subnet_ref(subnet_id) if subnet_id else None


def convert(source_data):
    """
    Converts ECS (Elastic Cloud Server) data to seaf.ta.components.server format.
    """
    ensure_prefix(source_data=source_data)
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
        tags_data = ecs_details.get('tags')
        if tags_data:
            tag_entries = []
            if isinstance(tags_data, list):
                for index, tag_item in enumerate(tags_data):
                    if isinstance(tag_item, dict):
                        key = tag_item.get('key')
                        value = tag_item.get('value')
                        if key is None or value is None:
                            collect_warning(f"{ecs_id}.tags[{index}]", 'value', "Missing 'key' or 'value' in tag dictionary. Skipping.")
                            continue
                        tag_entries.append(f"{key}:{value}")
                    elif isinstance(tag_item, str):
                        tag_entries.append(tag_item)
                    else:
                        collect_warning(f"{ecs_id}.tags[{index}]", 'value', f"Unsupported tag type '{type(tag_item).__name__}'. Skipping.")
            elif isinstance(tags_data, str):
                tag_entries.append(tags_data)
            else:
                collect_warning(ecs_id, 'tags', f"Unsupported tags type '{type(tags_data).__name__}'. Skipping tags.")
            if tag_entries:
                description_parts.append(f"Tags: {', '.join(tag_entries)}")
        if ecs_details.get('tenant'):
            description_parts.append(f"Tenant: {ecs_details.get('tenant')}")

        description = '\n'.join(description_parts).strip()

        # --- Disk Conversion with Warnings ---
        converted_disks = []
        disks_data = ecs_details.get('disks', [])
        if isinstance(disks_data, dict):
            disks_data = [disks_data]

        for disk_item in disks_data:
            if not isinstance(disk_item, dict):
                collect_warning(ecs_id, 'disks', f"Invalid disk item type '{type(disk_item).__name__}'. Expected dictionary. Skipping.")
                continue

            for disk_id, disk_props in disk_item.items():
                if not isinstance(disk_props, dict):
                    collect_warning(f"{ecs_id}.disks.{disk_id}", 'properties', f"Invalid disk properties type '{type(disk_props).__name__}'. Expected dictionary. Skipping.")
                    continue

                # Validate and parse size
                size_raw = disk_props.get('size')
                size_gb = 0
                if size_raw is None:
                    collect_warning(f"{ecs_id}.disks.{disk_id}", 'size', "Missing 'size' field. Defaulting to 0.")
                else:
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
                            collect_warning(f"{ecs_id}.disks.{disk_id}", 'size', f"Invalid numeric format for size '{size_raw}'. Defaulting to 0.")
                    else:
                        collect_warning(f"{ecs_id}.disks.{disk_id}", 'size', f"No numeric part found in size '{size_raw}'. Defaulting to 0.")
                
                # Validate AZ for disk
                disk_az_name = disk_props.get('az')
                if disk_az_name is None:
                    collect_warning(f"{ecs_id}.disks.{disk_id}", 'az', "Missing 'az' field for disk. Defaulting to None.")
                elif not isinstance(disk_az_name, str) or len(disk_az_name) <= 3:
                    collect_warning(f"{ecs_id}.disks.{disk_id}", 'az', f"Invalid AZ name '{disk_az_name}' (not a string or too short). Defaulting to None.")
                    disk_az_name = None # Ensure it's None if invalid

                converted_disks.append({
                    'az': find_dc_az_key(source_data, disk_az_name),
                    'size': size_gb,
                    'type': disk_props.get('type'), # No specific validation for type/device for now
                    'device': disk_props.get('device')
                })
        
        ram_mb = ecs_details.get('ram', 0)
        ram_gb = ram_mb // 1024 if ram_mb else 0

        # --- Location and AZ with Warnings ---
        az_ref = None
        az_name = ecs_details.get('az')
        location_ref = []
        if az_name is None:
            collect_warning(ecs_id, 'az', "Missing 'az' field for server. Location will be empty.")
        elif not isinstance(az_name, str) or len(az_name) <= 3:
            collect_warning(ecs_id, 'az', f"Invalid AZ name '{az_name}' (not a string or too short). Location will be empty.")
        else:
            az_ref = find_dc_az_key(source_data, az_name)
            location_ref = [dc_ref(az_name)]

        subnet_refs = [find_network_key(source_data, s_id) for s_id in ecs_details.get('subnets', [])]
        subnet_refs = [ref for ref in subnet_refs if ref]

        # --- CPU Frequency with Warnings ---
        freq_raw = cpu_details.get('frequency')
        freq_mhz = 0
        if freq_raw is None:
            collect_warning(ecs_id, 'cpu.frequency', "Missing 'frequency' field. Defaulting to 0.")
        else:
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
                    collect_warning(ecs_id, 'cpu.frequency', f"Invalid numeric format for frequency '{freq_raw}'. Defaulting to 0.")
            else:
                collect_warning(ecs_id, 'cpu.frequency', f"No numeric part found in frequency '{freq_raw}'. Defaulting to 0.")

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
            'virtualization': build_id('cluster_virtualization', 'cloud_ru_virtualization_cluster')
        }

    return {'seaf.ta.components.server': converted_servers}
