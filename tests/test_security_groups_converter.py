import unittest
import sys
import os
import json

# Add modules to the python path
sys.path.append(os.path.abspath('_metamodel_/iaas/converter/modules'))

from security_groups_converter import convert

class TestSecurityGroupsConverter(unittest.TestCase):

    def test_convert_security_groups(self):
        # Sample input data for Security Groups
        source_data = {
            'seaf.ta.reverse.cloud_ru.advanced.security_groups': {
                'flix.security_groups.0fdb3e4f-c7a6-42eb-9531-552ac5006202': {
                    'id': '0fdb3e4f-c7a6-42eb-9531-552ac5006202',
                    'name': 'sg-prod',
                    'description': 'blazing fast sg',
                    'rules': [
                        {
                            'description': 'perfect rule 1',
                            'direction': 'ingress',
                            'ethertype': 'IPv4',
                            'protocol_port': '22',
                            'protocol': 'tcp',
                            'remote_group_id': None,
                            'remote_ip_prefix': '10.10.0.10/32',
                            'remote_address_group_id': None
                        },
                        {
                            'description': 'Allow all traffic',
                            'direction': 'egress',
                            'ethertype': 'IPv4',
                            'protocol_port': 'All',
                            'protocol': None,
                            'remote_group_id': None,
                            'remote_ip_prefix': '0.0.0.0/0',
                            'remote_address_group_id': None
                        }
                    ],
                    'tenant': '9f7dcs8823ed23e9cwe223ecwe22236',
                    'DC': 'flix.dc.01'
                }
            }
        }

        # Expected output
        expected_output = {
            'seaf.ta.services.kb': {
                'flix.security_groups.0fdb3e4f-c7a6-42eb-9531-552ac5006202': {
                    'title': 'sg-prod',
                    'description': 'blazing fast sg\nTenant: 9f7dcs8823ed23e9cwe223ecwe22236\nDC: flix.dc.01\nRules: ' + json.dumps([
                        {
                            'description': 'perfect rule 1',
                            'direction': 'ingress',
                            'ethertype': 'IPv4',
                            'protocol_port': '22',
                            'protocol': 'tcp',
                            'remote_group_id': None,
                            'remote_ip_prefix': '10.10.0.10/32',
                            'remote_address_group_id': None
                        },
                        {
                            'description': 'Allow all traffic',
                            'direction': 'egress',
                            'ethertype': 'IPv4',
                            'protocol_port': 'All',
                            'protocol': None,
                            'remote_group_id': None,
                            'remote_ip_prefix': '0.0.0.0/0',
                            'remote_address_group_id': None
                        }
                    ], indent=2),
                    'external_id': '0fdb3e4f-c7a6-42eb-9531-552ac5006202',
                    'technology': 'Межсетевое экранирование',
                    'software_name': 'Cloud Security Group',
                    'tag': 'FW',
                    'status': 'Используется',
                    'network_connection': []
                }
            }
        }

        # Run the conversion
        converted_data = convert(source_data)

        # Assert that the result is as expected
        self.assertEqual(converted_data, expected_output)

if __name__ == '__main__':
    unittest.main()
