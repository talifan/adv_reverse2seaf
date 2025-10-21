# modules/vpcs_converter.py

def convert(source_data):
    """
    Converts VPC data to the target flix.vpcs format.
    """
    vpcs_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.vpcs', {})
    
    converted_vpcs = {}
    
    for vpc_id, vpc_details in vpcs_data.items():
        new_id = vpc_id
        
        description_parts = []
        if vpc_details.get('description'): # Include original description
            description_parts.append(vpc_details.get('description'))
        if vpc_details.get('cidr'):
            description_parts.append(f"CIDR: {vpc_details.get('cidr')}")
        if vpc_details.get('tenant'):
            description_parts.append(f"Tenant: {vpc_details.get('tenant')}")
        description = '\n'.join(description_parts)

        location = vpc_details.get('DC', '')

        converted_vpcs[new_id] = {
            'title': vpc_details.get('name'),
            'description': description,
            'external_id': vpc_details.get('id'),
            'sber': {
                'location': location,
                'zone': '###PLACEHOLDER_FOR_MANUAL_ZONE###'
            }
        }

    return {'seaf.ta.services.network_segment': converted_vpcs}
