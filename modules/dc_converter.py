# modules/dc_converter.py

def convert(source_data):
    """
    Creates a Data Center (DC) for each unique Availability Zone (AZ) found in the source data.
    """
    unique_azs = set()

    def add_az(az_source):
        if isinstance(az_source, str):
            if len(az_source) > 3:
                unique_azs.add(az_source)
        elif isinstance(az_source, list):
            for az_name in az_source:
                if isinstance(az_name, str) and len(az_name) > 3:
                    unique_azs.add(az_name)

    # Collect AZs from ECSs
    ecss_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.ecss', {})
    for ecs_details in ecss_data.values():
        add_az(ecs_details.get('az'))
        for disk_item in ecs_details.get('disks', []):
            if isinstance(disk_item, dict):
                for disk_props in disk_item.values():
                    if isinstance(disk_props, dict):
                        add_az(disk_props.get('az'))

    # Collect AZs from CCEs
    cces_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.cces', {})
    for cce_details in cces_data.values():
        add_az(cce_details.get('masters_az'))

    # Collect AZs from RDSs
    rdss_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.rdss', {})
    for rds_details in rdss_data.values():
        add_az(rds_details.get('az'))

    # Collect AZs from DMSs
    dmss_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.dmss', {})
    for dms_details in dmss_data.values():
        add_az(dms_details.get('available_az'))

    converted_dcs = {}
    for az_name in sorted(list(unique_azs)):
        dc_id = f"flix.dc.{az_name}"
        az_ref = f"flix.dc_az.{az_name}"

        converted_dcs[dc_id] = {
            'title': az_name,
            'external_id': az_name,
            'type': 'Облачный',
            'vendor': 'Cloud.ru',
            'address': az_name,
            'availabilityzone': az_ref
        }

    return {'seaf.ta.services.dc': converted_dcs}
