import unittest
import sys
import os

# Add modules and utils to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))

from id_prefix import set_prefix, segment_ref
from id_prefix import set_prefix, segment_ref
from rdss_converter import convert
from warning_reporter import get_collected_warnings, clear_collected_warnings

class TestRdssConverter(unittest.TestCase):

    def test_convert_rdss(self):
        set_prefix('tenant')
        # Sample input data
        source_data = {
            'seaf.ta.reverse.cloud_ru.advanced.subnets': {
                'tenant.subnets.0d9f37b6-0889-4763-8cf3-20d9641af0c1': {
                    'id': '0d9f37b6-0889-4763-8cf3-20d9641af0c1',
                    'name': 'subnet-Prod'
                }
            },
            'seaf.ta.reverse.cloud_ru.advanced.rdss': {
                'tenant.rdss.0e493e5847714a14a313e215d9e59b15in03': {
                    'id': '0e493e5847714a14a313e215d9e59b15in03',
                    'name': 'rds-prod-postgre',
                    'status': 'ACTIVE',
                    'type': 'Single',
                    'datastore': {
                        'type': 'PostgreSQL',
                        'version': '13',
                        'complete_version': '13.2.3'
                    },
                    'vpc_id': 'd48e294f-eb6a-4352-8d73-275b7a966e90',
                    'subnet_id': '0d9f37b6-0889-4763-8cf3-20d9641af0c1',
                    'volume': {
                        'type': 'ULTRAHIGH',
                        'size': 120
                    },
                    'private_ips': ['10.10.0.40'],
                    'public_ips': [],
                    'nodes': [
                        {
                            'id': '8ac72544860a4d50825cc307437d9b56no03',
                            'name': 'dms-prod-postgre_node0',
                            'role': 'master',
                            'status': 'ACTIVE',
                            'availability_zone': 'ru-moscow-1b'
                        }
                    ],
                    'flavor': 'rds.pg.c6.large.2',
                    'switch_strategy': '',
                    'backup_strategy': {
                        'start_time': '16:00-17:00',
                        'keep_days': 7
                    },
                    'tags': [],
                    'tenant': '9f7dcs8823ed23e9cwe223ecwe22236',
                    'DC': 'tenant.dc.01'
                }
            }
        }

        # Expected output
        expected_output = {
            'seaf.ta.services.cluster': {
                'tenant.rdss.0e493e5847714a14a313e215d9e59b15in03': {
                    'title': 'rds-prod-postgre',
                    'description': 'Status: ACTIVE\nFlavor: rds.pg.c6.large.2\nDatastore Type: PostgreSQL\nDatastore Version: 13\nDatastore Complete Version: 13.2.3\nVolume Type: ULTRAHIGH\nVolume Size (GB): 120\nNodes: Node ID: 8ac72544860a4d50825cc307437d9b56no03, Name: dms-prod-postgre_node0, Role: master, Status: ACTIVE, AZ: ru-moscow-1b\nBackup Start Time: 16:00-17:00\nBackup Keep Days: 7',
                    'external_id': '0e493e5847714a14a313e215d9e59b15in03',
                    'fqdn': '10.10.0.40',
                    'reservation_type': 'Single',
                    'service_type': 'СУБД',
                    'availabilityzone': ['tenant.dc_az.ru-moscow-1b'],
                    'location': ['tenant.dc.ru-moscow-1b'],
                    'network_connection': ['tenant.subnets.0d9f37b6-0889-4763-8cf3-20d9641af0c1'],
                    'segment': 'tenant.segment.ru-moscow-1b.INT-NET'
                }
            }
        }

        # Run the conversion
        clear_collected_warnings()
        converted_data = convert(source_data)

        # Assert that the result is as expected
        self.assertEqual(converted_data, expected_output)
        self.assertEqual(get_collected_warnings(), [])
        clear_collected_warnings()

    def test_convert_rdss_warnings(self):
        set_prefix('tenant')
        source_data = {
            'seaf.ta.reverse.cloud_ru.advanced.rdss': {
                'tenant.rdss.invalid': {
                    'id': 'invalid',
                    'name': 'invalid-rds',
                    'nodes': [],
                    'subnet_id': '',
                    # vpc_id intentionally omitted
                }
            }
        }

        expected_output = {
            'seaf.ta.services.cluster': {
                'tenant.rdss.invalid': {
                    'title': 'invalid-rds',
                    'description': '',
                    'external_id': 'invalid',
                    'fqdn': None,
                    'reservation_type': None,
                    'service_type': 'СУБД',
                    'availabilityzone': [],
                    'location': [],
                    'network_connection': [],
                    'segment': None
                }
            }
        }

        clear_collected_warnings()
        converted_data = convert(source_data)
        self.assertEqual(converted_data, expected_output)
        self.assertEqual(
            get_collected_warnings(),
            [
                "WARNING: Entity 'tenant.rdss.invalid' - Field 'nodes': Missing or empty 'nodes'. Availability zone and location will be empty.",
                "WARNING: Entity 'tenant.rdss.invalid' - Field 'subnet_id': Missing or empty 'subnet_id'. network_connection will be empty."
            ]
        )
        clear_collected_warnings()

if __name__ == '__main__':
    unittest.main()
