import unittest
import sys
import os

# Add modules to the python path
sys.path.append(os.path.abspath('_metamodel_/iaas/converter/modules'))

from rdss_converter import convert

class TestRdssConverter(unittest.TestCase):

    def test_convert_rdss(self):
        # Sample input data including VPCs and Subnets for linking
        source_data = {
            'seaf.ta.reverse.cloud_ru.advanced.vpcs': {
                'flix.vpcs.d48e294f-eb6a-4352-8d73-275b7a966e90': {
                    'id': 'd48e294f-eb6a-4352-8d73-275b7a966e90',
                    'name': 'vpc-internal'
                }
            },
            'seaf.ta.reverse.cloud_ru.advanced.subnets': {
                'flix.subnets.0d9f37b6-0889-4763-8cf3-20d9641af0c1': {
                    'id': '0d9f37b6-0889-4763-8cf3-20d9641af0c1',
                    'name': 'subnet-Prod',
                    'cidr': '10.10.0.0/24',
                    'vpc': 'd48e294f-eb6a-4352-8d73-275b7a966e90'
                }
            },
            'seaf.ta.reverse.cloud_ru.advanced.rdss': {
                'flix.rdss.0e493e5847714a14a313e215d9e59b15in03': {
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
                    'DC': 'flix.dc.01'
                }
            }
        }

        # Expected output
        expected_output = {
            'seaf.ta.services.cluster': {
                'flix.rdss.0e493e5847714a14a313e215d9e59b15in03': {
                    'title': 'rds-prod-postgre',
                    'description': 'Status: ACTIVE\nFlavor: rds.pg.c6.large.2\nDatastore Type: PostgreSQL\nDatastore Version: 13\nDatastore Complete Version: 13.2.3\nVolume Type: ULTRAHIGH\nVolume Size (GB): 120\nNodes: Node ID: 8ac72544860a4d50825cc307437d9b56no03, Name: dms-prod-postgre_node0, Role: master, Status: ACTIVE, AZ: ru-moscow-1b\nBackup Start Time: 16:00-17:00\nBackup Keep Days: 7',
                    'external_id': '0e493e5847714a14a313e215d9e59b15in03',
                    'fqdn': '10.10.0.40',
                    'reservation_type': 'Single',
                    'service_type': 'СУБД',
                    'availabilityzone': ['flix.dc_az.ru-moscow-1b'],
                    'location': ['flix.dc.01'],
                    'network_connection': ['flix.subnets.0d9f37b6-0889-4763-8cf3-20d9641af0c1']
                }
            }
        }

        # Run the conversion
        converted_data = convert(source_data)

        print(converted_data)

        # Assert that the result is as expected
        self.assertEqual(converted_data, expected_output)

if __name__ == '__main__':
    unittest.main()
