# modules/dc_az_converter.py

from id_prefix import ensure_prefix, build_id

def derive_region_from_az(az_name):
    """Derives the region name from an AZ name (e.g., 'ru-moscow-1c' -> 'ru-moscow-1')."""
    if az_name and len(az_name) > 1 and az_name[-1].isalpha():
        return az_name[:-1]
    return az_name # Return as is if not in expected format

def convert(source_data):
    """
    Collects unique AZs from various source entities and converts them to seaf.ta.services.dc_az format.
    """
    ensure_prefix(source_data=source_data)
    unique_azs = set()

    # Collect AZs from ECSs
    ecss_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.ecss', {})
    for ecs_id, ecs_details in ecss_data.items():
        az = ecs_details.get('az')
        if isinstance(az, str) and len(az) > 2:
            unique_azs.add(az)
        for disk_details in ecs_details.get('disks', []):
            if isinstance(disk_details, dict):
                disk_az = disk_details.get('az')
                if isinstance(disk_az, str) and len(disk_az) > 2:
                    unique_azs.add(disk_az)

    # Collect AZs from CCEs
    cces_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.cces', {})
    for cce_id, cce_details in cces_data.items():
        masters_az = cce_details.get('masters_az', [])
        for az in masters_az:
            if isinstance(az, str) and len(az) > 2:
                unique_azs.add(az)

    # Collect AZs from RDSs
    rdss_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.rdss', {})
    for rds_id, rds_details in rdss_data.items():
        az_list = rds_details.get('az', []) # RDS az is a list
        for az in az_list:
            if isinstance(az, str) and len(az) > 2:
                unique_azs.add(az)

    # Collect AZs from DMSs
    dmss_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.dmss', {})
    for dms_id, dms_details in dmss_data.items():
        available_az = dms_details.get('available_az', [])
        for az in available_az:
            if isinstance(az, str) and len(az) > 2:
                unique_azs.add(az)

    converted_dc_azs = {}
    for az_name in sorted(list(unique_azs)):
        # All AZs will reference the single 'Россия' region
        region_ref = build_id('dc_region', 'russia')

        # Construct the new ID for the dc_az entity
        # Example: ru-moscow-1c -> <prefix>.dc_az.ru-moscow-1c
        new_id = build_id('dc_az', az_name)

        converted_dc_azs[new_id] = {
            'title': az_name,
            'external_id': az_name, # Using az_name as external_id for now
            'vendor': 'Cloud.ru',
            'region': region_ref
        }

    return {'seaf.ta.services.dc_az': converted_dc_azs}
