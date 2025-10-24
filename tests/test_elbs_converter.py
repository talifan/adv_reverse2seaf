import unittest
import sys
import os
import json

# Add modules to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))

from id_prefix import set_prefix, segment_ref
from id_prefix import set_prefix, segment_ref
from elbs_converter import convert

class TestElbsConverter(unittest.TestCase):

    def test_convert_elbs(self):
        set_prefix('tenant')
        # Sample input data including Subnets for linking
        source_data = {
            'seaf.ta.reverse.cloud_ru.advanced.subnets': {
                'tenant.subnets.6b2820d7-17c6-409a-91cb-b634cf596fdb': {
                    'id': '6b2820d7-17c6-409a-91cb-b634cf596fdb',
                    'name': 'subnet-Test',
                    'cidr': '10.10.10.0/24',
                    'vpc': 'd48e294f-eb6a-4352-8d73-275b7a966e90',
                    'availability_zone': 'ru-moscow-1a',
                    'DC': 'tenant.dc.ru-moscow-1a'
                }
            },
            'seaf.ta.reverse.cloud_ru.advanced.elbs': {
                'tenant.elbs.6d174721-db0e-4758-9a96-2f626e1a6632': {
                    'id': '6d174721-db0e-4758-9a96-2f626e1a6632',
                    'name': 'elb-ingress-test',
                    'description': 'Test ELB for ingress',
                    'subnet_id': '6b2820d7-17c6-409a-91cb-b634cf596fdb',
                    'port_id': '18f854e2-1189-44ba-ab12-ddf88d788de7',
                    'address': '10.10.10.30',
                    'operating_status': 'ONLINE',
                    'provisioning_status': 'ACTIVE',
                    'listeners': [
                        {
                            'id': 'a230fdde-fe28-48dd-88a4-59926d9623b0',
                            'name': 'listener-1b3e',
                            'default_pool_id': 'c247be56-3483-4f05-bbff-19705bf3f81c',
                            'protocol_port': 80,
                            'protocol': 'TCP'
                        }
                    ],
                    'pools': [
                        {
                            'id': 'c247be56-3483-4f05-bbff-19705bf3f81c',
                            'name': 'server_group-1',
                            'lb_algorithm': 'ROUND_ROBIN',
                            'members': []
                        }
                    ],
                    'tags': [],
                    'forwardingpolicy': [],
                    'tenant': '9f7dcs8823ed23e9cwe223ecwe22236',
                    'DC': 'tenant.dc.01'
                }
            },
            'seaf.ta.reverse.cloud_ru.advanced.ecss': {}
        }

        # Expected output
        listeners_json = json.dumps([
            {
                'id': 'a230fdde-fe28-48dd-88a4-59926d9623b0',
                'name': 'listener-1b3e',
                'default_pool_id': 'c247be56-3483-4f05-bbff-19705bf3f81c',
                'protocol_port': 80,
                'protocol': 'TCP'
            }
        ], indent=2)
        pools_json = json.dumps([
            {
                'id': 'c247be56-3483-4f05-bbff-19705bf3f81c',
                'name': 'server_group-1',
                'lb_algorithm': 'ROUND_ROBIN',
                'members': []
            }
        ], indent=2)

        expected_output = {
            'seaf.ta.services.compute_service': {
                'tenant.elbs.6d174721-db0e-4758-9a96-2f626e1a6632': {
                    'title': 'elb-ingress-test',
                    'description': 'Test ELB for ingress\nInternal IP: 10.10.10.30\nOperating Status: ONLINE\nProvisioning Status: ACTIVE\nTenant: 9f7dcs8823ed23e9cwe223ecwe22236\nListeners: ' + listeners_json + '\nPools: ' + pools_json + '\nDC: tenant.dc.ru-moscow-1a',
                    'external_id': '6d174721-db0e-4758-9a96-2f626e1a6632',
                    'availabilityzone': ['tenant.dc_az.ru-moscow-1a'],
                    'location': ['tenant.dc.ru-moscow-1a'],
                    'network_connection': ['tenant.subnets.6b2820d7-17c6-409a-91cb-b634cf596fdb'],
                    'service_type': 'Шлюз, Балансировщик, прокси'
                }
            }
        }

        # Run the conversion
        converted_data = convert(source_data)

        # Assert that the result is as expected
        self.assertEqual(converted_data, expected_output)

if __name__ == '__main__':
    unittest.main()
