# modules/dc_region_converter.py

from dc_az_converter import derive_region_from_az # Import helper from dc_az_converter

def convert(source_data):
    """
    Creates a single 'Россия' region entity (seaf.ta.services.dc_region).
    """
    converted_dc_regions = {}
    
    # Create a single region entity for 'Россия'
    region_id = 'russia'
    new_id = f"flix.dc_region.{region_id}"

    converted_dc_regions[new_id] = {
        'title': 'Россия',
        'external_id': region_id,
    }

    return {'seaf.ta.services.dc_region': converted_dc_regions}
