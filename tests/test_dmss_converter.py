import unittest
import sys
import os

# Add modules to the python path
sys.path.append(os.path.abspath('_metamodel_/iaas/converter/modules'))

from dmss_converter import convert

class TestDmssConverter(unittest.TestCase):

    def test_convert_dmss(self):
        # Sample input data including VPCs and Subnets for linking
        source_data = {
            'seaf.ta.reverse.cloud_ru.advanced.vpcs': {
                'flix.vpcs.d48e294f-eb6a-4352-8d73-275b7a966e90': {
                    'id': 'd48e294f-eb6a-4352-8d73-275b7a966e90',
                    'name': 'vpc-internal'
                }
            },
            'seaf.ta.reverse.cloud_ru.advanced.subnets': {
                'flix.subnets.6b2820d7-17c6-409a-91cb-b634cf596fdb': {
                    'id': '6b2820d7-17c6-409a-91cb-b634cf596fdb',
                    'name': 'subnet-Test',
                    'cidr': '10.10.10.0/24',
                    'vpc': 'd48e294f-eb6a-4352-8d73-275b7a966e90'
                }
            },
            'seaf.ta.reverse.cloud_ru.advanced.dmss': {
                'flix.dmss.7bb3c551-0fc3-4916-a853-302390af0569': {
                    'id': '7bb3c551-0fc3-4916-a853-302390af0569',
                    'name': 'dms-rabbitmq-test',
                    'engine': 'rabbitmq',
                    'engine_version': '3.7.17',
                    'port': '5672',
                    'address': '10.10.10.20',
                    'vpc_id': 'd48e294f-eb6a-4352-8d73-275b7a966e90',
                    'subnet_id': '6b2820d7-17c6-409a-91cb-b634cf596fdb',
                    'status': 'RUNNING',
                    'type': 'single',
                    'specification': '2vCPUs 4GB',
                    'security_groups': ['0fdb3e4f-c7a6-42eb-9531-552ac5006202'],
                    'available_az': ['ru-moscow-1a'],
                    'storage_space': '177',
                    'total_storage_space': '200',
                    'used_storage_space': '0',
                    'storage_spec_code': 'dms.physical.storage.high',
                    'management': 'http://10.10.10.20:15672',
                    'support_features': 'auto.create.topics.enable,rabbitmq.plugin.management',
                    'node_num': 1,
                    'disk_encrypted': False,
                    'tenant': '9f7dcs8823ed23e9cwe223ecwe22236',
                    'DC': 'flix.dc.01'
                }
            }
        }

        # Expected output
        expected_output = {
            'seaf.ta.services.cluster': {
                'flix.dmss.7bb3c551-0fc3-4916-a853-302390af0569': {
                    'title': 'dms-rabbitmq-test',
                    'description': 'Engine: rabbitmq\nEngine Version: 3.7.17\nPort: 5672\nStatus: RUNNING\nSpecification: 2vCPUs 4GB\nSecurity Groups: 0fdb3e4f-c7a6-42eb-9531-552ac5006202\nStorage Space: 177\nTotal Storage Space: 200\nUsed Storage Space: 0\nStorage Spec Code: dms.physical.storage.high\nManagement URL: http://10.10.10.20:15672\nSupported Features: auto.create.topics.enable,rabbitmq.plugin.management\nNode Num: 1\nDisk Encrypted: False\nTenant: 9f7dcs8823ed23e9cwe223ecwe22236\nDC: flix.dc.01',
                    'external_id': '7bb3c551-0fc3-4916-a853-302390af0569',
                    'fqdn': '10.10.10.20',
                    'reservation_type': 'single',
                    'service_type': 'Интеграционная шина  (MQ, ETL, API)',
                    'availabilityzone': ['flix.dc_az.ru-moscow-1a'],
                    'location': ['flix.dc.ru-moscow-1a'],
                    'network_connection': ['flix.subnets.6b2820d7-17c6-409a-91cb-b634cf596fdb']
                }
            }
        }

        # Run the conversion
        converted_data = convert(source_data)

        # Assert that the result is as expected
        self.assertEqual(converted_data, expected_output)

if __name__ == '__main__':
    unittest.main()
