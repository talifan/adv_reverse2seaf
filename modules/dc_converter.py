# modules/dc_converter.py

from warning_reporter import collect_warning # Import for collecting warnings
from id_prefix import ensure_prefix, dc_ref, dc_az_ref

def convert(source_data):
    """
    Creates a Data Center (DC) for each unique Availability Zone (AZ) found in the source data.
    """
    ensure_prefix(source_data=source_data)
    unique_azs = set()

    def add_az(entity_id, field_name, az_source):
        if az_source is None:
            return
        
        if isinstance(az_source, str):
            if len(az_source) > 3:
                unique_azs.add(az_source)
            else:
                collect_warning(entity_id, field_name, f"Invalid AZ name '{az_source}' (too short). Skipping.")
        elif isinstance(az_source, list):
            for az_name in az_source:
                if isinstance(az_name, str):
                    if len(az_name) > 3:
                        unique_azs.add(az_name)
                    else:
                        collect_warning(entity_id, field_name, f"Invalid AZ name '{az_name}' (too short) in list. Skipping.")
                else:
                    collect_warning(entity_id, field_name, f"Invalid AZ entry '{az_name}' (not a string) in list. Skipping.")
        else:
            collect_warning(entity_id, field_name, f"Invalid AZ source type '{type(az_source).__name__}'. Expected string or list. Skipping.")

    # Collect AZs from ECSs
    ecss_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.ecss', {})
    for ecs_id, ecs_details in ecss_data.items(): # Added ecs_id for reporting
        add_az(ecs_id, 'az', ecs_details.get('az'))
        for disk_item in ecs_details.get('disks', []):
            if isinstance(disk_item, dict):
                for disk_id, disk_props in disk_item.items(): # Added disk_id for reporting
                    if isinstance(disk_props, dict):
                        add_az(f"{ecs_id}.disks.{disk_id}", 'az', disk_props.get('az'))

    # Collect AZs from CCEs
    cces_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.cces', {})
    for cce_id, cce_details in cces_data.items(): # Added cce_id for reporting
        add_az(cce_id, 'masters_az', cce_details.get('masters_az'))

    # Collect AZs from RDSs
    rdss_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.rdss', {})
    for rds_id, rds_details in rdss_data.items(): # Added rds_id for reporting
        add_az(rds_id, 'az', rds_details.get('az'))

    # Collect AZs from DMSs
    dmss_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.dmss', {})
    for dms_id, dms_details in dmss_data.items(): # Added dms_id for reporting
        add_az(dms_id, 'available_az', dms_details.get('available_az'))

    converted_dcs = {}
    for az_name in sorted(list(unique_azs)):
        dc_id = dc_ref(az_name)
        az_ref = dc_az_ref(az_name)

        converted_dcs[dc_id] = {
            'title': az_name,
            'external_id': az_name,
            'type': 'Облачный',
            'vendor': 'Cloud.ru',
            'address': az_name,
            'availabilityzone': az_ref
        }

    return {'seaf.ta.services.dc': converted_dcs}
