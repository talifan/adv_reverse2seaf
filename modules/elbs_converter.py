# modules/elbs_converter.py
import json # For dumping listeners and pools to description

def find_network_key(source_data, subnet_id):
    """Finds the full key for a Network from its subnet ID."""
    return f"flix.subnets.{subnet_id}" if subnet_id else None

def find_network_segment_key_from_subnet(source_data, subnet_id):
    """Finds the network segment key by looking up the subnet's VPC."""
    if not subnet_id:
        return None
    
    subnets_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.subnets', {})
    
    # Find the subnet details by iterating through the subnets data
    found_subnet = None
    for subnet_key, subnet_details in subnets_data.items():
        if subnet_details.get('id') == subnet_id:
            found_subnet = subnet_details
            break

    if found_subnet:
        vpc_id = found_subnet.get('vpc')
        if vpc_id:
            # Assuming VPCs are converted to network_segments and their key is based on the vpc_id
            return f"flix.vpcs.{vpc_id}"
    return None

def convert(source_data):
    """
    Converts ELB (Elastic Load Balancer) data to seaf.ta.components.network format.
    """
    elbs_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.elbs', {})
    
    converted_networks = {}
    
    for elb_id, elb_details in elbs_data.items():
        new_id = elb_id
        
        description_parts = []
        if elb_details.get('description'):
            description_parts.append(elb_details.get('description'))
        if elb_details.get('address'):
            description_parts.append(f"Internal IP: {elb_details.get('address')}")
        if elb_details.get('operating_status'):
            description_parts.append(f"Operating Status: {elb_details.get('operating_status')}")
        if elb_details.get('provisioning_status'):
            description_parts.append(f"Provisioning Status: {elb_details.get('provisioning_status')}")
        if elb_details.get('tags'):
            tags_str = ', '.join([f"{tag['key']}:{tag['value']}" for tag in elb_details.get('tags')])
            description_parts.append(f"Tags: {tags_str}")
        if elb_details.get('tenant'):
            description_parts.append(f"Tenant: {elb_details.get('tenant')}")
        if elb_details.get('DC'):
            description_parts.append(f"DC: {elb_details.get('DC')}")

        # Add listeners and pools to description as JSON for now
        listeners = elb_details.get('listeners', [])
        if listeners:
            description_parts.append(f"Listeners: {json.dumps(listeners, indent=2)}")
        pools = elb_details.get('pools', [])
        if pools:
            description_parts.append(f"Pools: {json.dumps(pools, indent=2)}")

        description = '\n'.join(description_parts).strip()

        # Resolve network_connection (subnet_id)
        subnet_id = elb_details.get('subnet_id')
        network_connection_refs = []
        if subnet_id:
            network_connection_refs.append(find_network_key(source_data, subnet_id))
        network_connection_refs = [ref for ref in network_connection_refs if ref] # Filter out None values

        # Resolve segment from subnet_id
        segment_ref = find_network_segment_key_from_subnet(source_data, subnet_id)

        converted_networks[new_id] = {
            'title': elb_details.get('name'),
            'description': description,
            'external_id': elb_details.get('id'),
            'model': 'Cloud ELB', # Default value
            'realization_type': 'Виртуальный', # Fixed value for ELB
            'type': 'Маршрутизатор', # Fixed value for ELB
            'network_connection': network_connection_refs,
            'segment': segment_ref,
            'location': [elb_details.get('DC')] if elb_details.get('DC') else [],
            'address': elb_details.get('address') # Internal IP
        }

    return {'seaf.ta.components.network': converted_networks}
