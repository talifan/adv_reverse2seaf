import unittest
import sys
import os

# Add modules and utils to the python path
sys.path.append(os.path.abspath('_metamodel_/iaas/converter/modules'))
sys.path.append(os.path.abspath('_metamodel_/iaas/converter/utils'))

from cces_converter import convert
from warning_reporter import get_collected_warnings, clear_collected_warnings

class TestCcesConverter(unittest.TestCase):

    def test_convert_cces(self):
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
            'seaf.ta.reverse.cloud_ru.advanced.cces': {
                'flix.cces.a8350fe7-cfdd-11ed-9fc0-0255ac100088': {
                    'name': 'cce-test',
                    'id': 'a8350fe7-cfdd-11ed-9fc0-0255ac100088',
                    'alias': 'cce-dev',
                    'flavor': 'cce.s1.small',
                    'version': 'v1.23',
                    'platform_version': 'cce.8.0',
                    'vpc_id': 'd48e294f-eb6a-4352-8d73-275b7a966e90',
                    'subnet_id': '6b2820d7-17c6-409a-91cb-b634cf596fdb',
                    'addresses': ['10.10.10.10'],
                    'security_groups': ['0fdb3e4f-c7a6-42eb-9531-552ac5006202'],
                    'container_network': '172.16.0.0/16',
                    'service_network': '10.34.0.0/16',
                    'authentication': 'rbac',
                    'masters_az': ['ru-moscow-1c'],
                    'supportistio': True,
                    'endpoints': [
                        {'url': 'https://10.10.10.10:5443', 'type': 'Internal'}
                    ],
                    'tenant': '9f7dcs8823ed23e9cwe223ecwe22236',
                    'DC': 'flix.dc.01'
                }
            }
        }

        # Expected output
        expected_output = {
            'seaf.ta.services.k8s': {
                'flix.cces.a8350fe7-cfdd-11ed-9fc0-0255ac100088': {
                    'title': 'cce-test',
                    'description': 'Flavor: cce.s1.small\nPlatform Version: cce.8.0\nIP Addresses: 10.10.10.10\nSecurity Groups: 0fdb3e4f-c7a6-42eb-9531-552ac5006202\nContainer Network: 172.16.0.0/16\nTenant: 9f7dcs8823ed23e9cwe223ecwe22236\nAlias: cce-dev',
                    'external_id': 'a8350fe7-cfdd-11ed-9fc0-0255ac100088',
                    'fqdn': 'https://10.10.10.10:5443',
                    'software': 'CCE v1.23',
                    'availabilityzone': ['flix.dc_az.ru-moscow-1c'],
                    'location': ['flix.dc.ru-moscow-1c'],
                    'service_mesh': 'istio',
                    'network_connection': ['flix.subnets.6b2820d7-17c6-409a-91cb-b634cf596fdb'],
                    'management_networks': ['cidr.10_34_0_0_16'],
                    'auth': 'flix.kb.idp.rbac',
                    'is_own': None,
                    'cni': None,
                    'cluster_autoscaler': None,
                    'keys': None,
                    'idm': None,
                    'policy': None,
                    'pam': None,
                    'ca': None,
                    'audit': None,
                    'audit_policy': None,
                    'monitoring': [],
                    'backup': [],
                    'registries': []
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

    def test_convert_cces_warnings(self):
        source_data = {
            'seaf.ta.reverse.cloud_ru.advanced.cces': {
                'flix.cces.invalid': {
                    'id': 'invalid',
                    'name': 'invalid-cluster',
                    'masters_az': 'ru',  # invalid (too short)
                    'subnet_id': None
                }
            }
        }

        expected_output = {
            'seaf.ta.services.k8s': {
                'flix.cces.invalid': {
                    'title': 'invalid-cluster',
                    'description': '',
                    'external_id': 'invalid',
                    'fqdn': None,
                    'software': None,
                    'availabilityzone': [],
                    'location': [],
                    'service_mesh': None,
                    'network_connection': [],
                    'management_networks': [],
                    'auth': None,
                    'is_own': None,
                    'cni': None,
                    'cluster_autoscaler': None,
                    'keys': None,
                    'idm': None,
                    'policy': None,
                    'pam': None,
                    'ca': None,
                    'audit': None,
                    'audit_policy': None,
                    'monitoring': [],
                    'backup': [],
                    'registries': []
                }
            }
        }

        clear_collected_warnings()
        converted_data = convert(source_data)
        self.assertEqual(converted_data, expected_output)
        self.assertEqual(
            get_collected_warnings(),
            [
                "WARNING: Entity 'flix.cces.invalid.masters_az' - Field 'value': Invalid AZ value 'ru'. Skipping.",
                "WARNING: Entity 'flix.cces.invalid' - Field 'masters_az': No valid AZ values found. Location will be empty.",
                "WARNING: Entity 'flix.cces.invalid' - Field 'subnet_id': Missing or empty 'subnet_id'. network_connection will be empty."
            ]
        )
        clear_collected_warnings()

if __name__ == '__main__':
    unittest.main()
