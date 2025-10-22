# modules/rdss_converter.py

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
    Converts RDS (Relational Database Service) data to seaf.ta.services.cluster format.
    """
    rdss_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.rdss', {})
    
    converted_clusters = {}
    
    for rds_id, rds_details in rdss_data.items():
        new_id = rds_id
        
        description_parts = []
        # Order: Status, Flavor, Datastore, Volume, Nodes, Backup Strategy
        if rds_details.get('status'):
            description_parts.append(f"Status: {rds_details.get('status')}")
        if rds_details.get('flavor'):
            description_parts.append(f"Flavor: {rds_details.get('flavor')}")
        
        # Datastore details
        datastore = rds_details.get('datastore', {})
        if datastore:
            description_parts.append(f"Datastore Type: {datastore.get('type')}")
            description_parts.append(f"Datastore Version: {datastore.get('version')}")
            if datastore.get('complete_version'):
                description_parts.append(f"Datastore Complete Version: {datastore.get('complete_version')}")

        # Volume details
        volume = rds_details.get('volume', {})
        if volume:
            description_parts.append(f"Volume Type: {volume.get('type')}")
            description_parts.append(f"Volume Size (GB): {volume.get('size')}")

        # Nodes details
        nodes = rds_details.get('nodes', [])
        if nodes:
            node_info = []
            for node in nodes:
                node_info.append(f"Node ID: {node.get('id')}, Name: {node.get('name')}, Role: {node.get('role')}, Status: {node.get('status')}, AZ: {node.get('availability_zone')}")
            description_parts.append(f"Nodes: {'; '.join(node_info)}")

        # Backup strategy
        backup_strategy = rds_details.get('backup_strategy', {})
        if backup_strategy:
            description_parts.append(f"Backup Start Time: {backup_strategy.get('start_time')}")
            description_parts.append(f"Backup Keep Days: {backup_strategy.get('keep_days')}")
        
        # Removed other fields from description that are not in expected output
        # if rds_details.get('description'):
        #     description_parts.append(rds_details.get('description'))
        # if rds_details.get('public_ips'):
        #     description_parts.append(f"Public IPs: {', '.join(rds_details.get('public_ips'))}")
        # if rds_details.get('tags'):
        #     tags_str = ', '.join([f"{tag['key']}:{tag['value']}" for tag in rds_details.get('tags')])
        #     description_parts.append(f"Tags: {tags_str}")
        # if rds_details.get('tenant'):
        #     description_parts.append(f"Tenant: {rds_details.get('tenant')}")
        # if rds_details.get('switch_strategy'):
        #     description_parts.append(f"Switch Strategy: {rds_details.get('switch_strategy')}")

        description = '\n'.join(description_parts).strip()

        # Collect AZs from nodes
        unique_node_azs = set()
        nodes = rds_details.get('nodes', [])
        for node in nodes:
            node_az = node.get('availability_zone')
            if isinstance(node_az, str) and len(node_az) > 2:
                unique_node_azs.add(node_az)

        # Resolve AZ references from collected node AZs
        az_refs = [find_dc_az_key(source_data, az_name) for az_name in sorted(list(unique_node_azs))]
        az_refs = [ref for ref in az_refs if ref] # Filter out None values

        # Resolve location (DC) based on collected node AZs
        location_refs = [f"flix.dc.{az_name}" for az_name in sorted(list(unique_node_azs)) if az_name]
        location_refs = [ref for ref in location_refs if ref] # Filter out None values

        # Resolve network_connection (subnet_id)
        network_connection_refs = []
        subnet_id = rds_details.get('subnet_id')
        if subnet_id:
            network_connection_refs.append(find_network_key(source_data, subnet_id))
        network_connection_refs = [ref for ref in network_connection_refs if ref] # Filter out None values

        converted_clusters[new_id] = {
            'title': rds_details.get('name'),
            'description': description,
            'external_id': rds_details.get('id'),
            'fqdn': rds_details.get('private_ips')[0] if rds_details.get('private_ips') else None,
            'reservation_type': rds_details.get('type'),
            'service_type': 'СУБД', # Fixed value for RDS
            'availabilityzone': az_refs,
            'location': location_refs,
            'network_connection': network_connection_refs,
        }

    return {'seaf.ta.services.cluster': converted_clusters}
