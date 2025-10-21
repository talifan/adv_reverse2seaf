# modules/security_groups_converter.py
import json

def convert(source_data):
    """
    Converts Security Groups data to seaf.ta.services.kb format.
    """
    security_groups_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.security_groups', {})
    
    converted_kbs = {}
    
    for sg_id, sg_details in security_groups_data.items():
        new_id = sg_id
        
        description_parts = []
        if sg_details.get('description'):
            description_parts.append(sg_details.get('description'))
        if sg_details.get('tenant'):
            description_parts.append(f"Tenant: {sg_details.get('tenant')}")
        if sg_details.get('DC'):
            description_parts.append(f"DC: {sg_details.get('DC')}")

        rules = sg_details.get('rules', [])
        if rules:
            description_parts.append(f"Rules: {json.dumps(rules, indent=2)}")

        description = '\n'.join(description_parts).strip()

        converted_kbs[new_id] = {
            'title': sg_details.get('name'),
            'description': description,
            'external_id': sg_details.get('id'),
            'technology': 'Межсетевое экранирование',
            'software_name': 'Cloud Security Group',
            'tag': 'FW',
            'status': 'Используется',
            'network_connection': [], # Not directly available in source
        }

    return {'seaf.ta.services.kb': converted_kbs}
