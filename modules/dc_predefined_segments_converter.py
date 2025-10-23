# modules/dc_predefined_segments_converter.py

from id_prefix import ensure_prefix, dc_ref, segment_ref

PREDEFINED_SEGMENTS = [
    "EXTERNAL-NET",
    "INTERNET",
    "TRANSPORT-WAN",
    "INET-EDGE",
    "EXT-WAN-EDGE",
    "INT-WAN-EDGE",
    "DMZ",
    "INT-NET",
    "INT-SECURITY-NET"
]

def convert(source_data):
    """
    Creates a predefined set of network segments for each data center.
    """
    ensure_prefix(source_data=source_data)
    dcs_data = source_data.get('seaf.ta.services.dc', {})
    
    converted_segments = {}
    
    for dc_id_full, dc_details in dcs_data.items():
        dc_id = dc_id_full.split('.')[-1] # Extract simple DC ID
        dc_title = dc_details.get('title', dc_id)
        for segment_name in PREDEFINED_SEGMENTS:
            segment_id = segment_ref(dc_id, segment_name)
            
            converted_segments[segment_id] = {
                'title': f'{segment_name} ({dc_title})',
                'description': f'Predefined network segment {segment_name} for data center {dc_title}',
                'external_id': f'segment_{dc_id}_{segment_name}',
                'location': dc_ref(dc_id),
                'type': 'Default', # Or determine based on name if needed
                'zone': segment_name
            }

    return {'seaf.ta.services.network_segment': converted_segments}
