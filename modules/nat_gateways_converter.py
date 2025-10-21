# modules/nat_gateways_converter.py
import json # For dumping rules to description

def find_network_key(source_data, subnet_id):
    """Finds the full key for a Network from its subnet ID."""
    return f"flix.subnets.{subnet_id}" if subnet_id else None

def convert(source_data):
    """
    Converts NAT Gateway data to seaf.ta.components.network format.
    """
    nat_gateways_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.nat_gateways', {})
    
    converted_networks = {}
    
    for nat_id, nat_details in nat_gateways_data.items():
        new_id = nat_id
        
        description_parts = []
        if nat_details.get('description'):
            description_parts.append(nat_details.get('description'))
        if nat_details.get('address'):
            description_parts.append(f"Internal IP: {nat_details.get('address')}")
        if nat_details.get('status'):
            description_parts.append(f"Status: {nat_details.get('status')}")
        if nat_details.get('tenant'):
            description_parts.append(f"Tenant: {nat_details.get('tenant')}")
        if nat_details.get('DC'):
            description_parts.append(f"DC: {nat_details.get('DC')}")

        # Add SNAT and DNAT rules to description as JSON for now
        snat_rules = nat_details.get('snat_rules', [])
        if snat_rules:
            description_parts.append(f"SNAT Rules: {json.dumps(snat_rules, indent=2)}")
        dnat_rules = nat_details.get('dnat_rules', [])
        description_parts.append(f"DNAT Rules: {json.dumps(dnat_rules, indent=2)}")

        description = '\n'.join(description_parts).strip()

        # Resolve network_connection (subnet_id)
        network_connection_refs = []
        subnet_id = nat_details.get('subnet_id')
        if subnet_id:
            network_connection_refs.append(find_network_key(source_data, subnet_id))
        network_connection_refs = [ref for ref in network_connection_refs if ref] # Filter out None values

        converted_networks[new_id] = {
            'title': nat_details.get('name'),
            'description': description,
            'external_id': nat_details.get('id'),
            'model': 'Cloud NAT Gateway', # Default value
            'realization_type': 'Виртуальный', # Fixed value for NAT Gateway
            'type': 'NAT', # Fixed value for NAT Gateway
            'network_connection': network_connection_refs,
            'location': [nat_details.get('DC')] if nat_details.get('DC') else [],
            'address': nat_details.get('address') # Internal IP
        }

    return {'seaf.ta.components.network': converted_networks}
