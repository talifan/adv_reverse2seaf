# modules/branches_converter.py

from id_prefix import ensure_prefix, build_id


def find_dc_region_key(source_data, country, city):
    """Finds or constructs a key for a DC Region based on country and city."""
    # This is a simplification. In a real scenario, we would have a mapping or a way to look up DC Regions.
    if country and city:
        region_key = f"{country.lower().replace(' ', '_')}_{city.lower().replace(' ', '_')}"
        return build_id('dc_region', region_key)
    return None

def convert(source_data):
    """
    Converts Branches data to seaf.ta.services.office format.
    """
    ensure_prefix(source_data=source_data)
    branches_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.branches', {})
    
    converted_offices = {}
    
    for branch_id, branch_details in branches_data.items():
        new_id = branch_id
        
        description_parts = []
        if branch_details.get('symbol'):
            description_parts.append(f"Symbol: {branch_details.get('symbol')}")

        description = '\n'.join(description_parts).strip()

        # Resolve region reference
        region_ref = find_dc_region_key(source_data, branch_details.get('country'), branch_details.get('city'))

        converted_offices[new_id] = {
            'title': branch_details.get('name'),
            'description': description,
            'external_id': branch_details.get('id'),
            'address': branch_details.get('location'),
            'region': region_ref,
        }

    return {'seaf.ta.services.office': converted_offices}
