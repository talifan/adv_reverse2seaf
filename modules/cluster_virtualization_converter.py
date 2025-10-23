# modules/cluster_virtualization_converter.py

from ecss_converter import find_network_key # Assuming ecss_converter has this helper
from id_prefix import ensure_prefix, dc_az_ref, build_id

def convert(source_data):
    """
    Creates a single cluster_virtualization entity and links it to relevant AZs and networks.
    """
    ensure_prefix(source_data=source_data)
    converted_cluster_virtualization = {}
    
    unique_azs = set()
    unique_network_connections = set()

    # Collect AZs and network connections from ECSs
    ecss_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.ecss', {})
    for ecs_id, ecs_details in ecss_data.items():
        az = ecs_details.get('az')
        if isinstance(az, str) and len(az) > 2:
            unique_azs.add(dc_az_ref(az))
        
        for disk_details in ecs_details.get('disks', []):
            if isinstance(disk_details, dict):
                disk_az = disk_details.get('az')
                if isinstance(disk_az, str) and len(disk_az) > 2:
                    unique_azs.add(dc_az_ref(disk_az))

        for subnet_id in ecs_details.get('subnets', []):
            if subnet_id:
                unique_network_connections.add(find_network_key(source_data, subnet_id))

    # Filter out None values from collected sets
    unique_azs = {az for az in unique_azs if az}
    unique_network_connections = {net for net in unique_network_connections if net}

    # Create the single cluster_virtualization entity if there are any VMs
    if ecss_data:
        cluster_id = "cloud_ru_virtualization_cluster"
        new_id = build_id("cluster_virtualization", cluster_id)

        converted_cluster_virtualization[new_id] = {
            'title': 'Cloud.ru Virtualization Cluster',
            'external_id': cluster_id,
            'hypervisor': 'Cloud.ru Hypervisor',
            'availabilityzone': sorted(list(unique_azs)),
            'location': [], # Not available in source
            'network_connection': sorted(list(unique_network_connections)),
        }

    return {'seaf.ta.services.cluster_virtualization': converted_cluster_virtualization}
