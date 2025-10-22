import unittest
import sys
import os
import json

# Add modules to the python path
sys.path.append(os.path.abspath('_metamodel_/iaas/converter/modules'))

from elbs_converter import convert

class TestElbsConverter(unittest.TestCase):

    def test_convert_elbs(self):
        # Sample input data including Subnets and VPCs for linking
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
            'seaf.ta.reverse.cloud_ru.advanced.elbs': {
                'flix.elbs.6d174721-db0e-4758-9a96-2f626e1a6632': {
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
                    'DC': 'flix.dc.01'
                }
            }
        }

        # Expected output
        expected_output = {
            'seaf.ta.components.network': {
                'flix.elbs.6d174721-db0e-4758-9a96-2f626e1a6632': {
                    'title': 'elb-ingress-test',
                    'description': 'Test ELB for ingress\nInternal IP: 10.10.10.30\nOperating Status: ONLINE\nProvisioning Status: ACTIVE\nTenant: 9f7dcs8823ed23e9cwe223ecwe22236\nDC: flix.dc.01\nListeners: ' + json.dumps([
                        {
                            'id': 'a230fdde-fe28-48dd-88a4-59926d9623b0',
                            'name': 'listener-1b3e',
                            'default_pool_id': 'c247be56-3483-4f05-bbff-19705bf3f81c',
                            'protocol_port': 80,
                            'protocol': 'TCP'
                        }
                    ], indent=2) + '\nPools: ' + json.dumps([
                        {
                            'id': 'c247be56-3483-4f05-bbff-19705bf3f81c',
                            'name': 'server_group-1',
                            'lb_algorithm': 'ROUND_ROBIN',
                            'members': []
                        }
                    ], indent=2),
                    'external_id': '6d174721-db0e-4758-9a96-2f626e1a6632',
                    'model': 'Cloud ELB',
                    'realization_type': 'Виртуальный',
                    'type': 'Маршрутизатор',
                    'network_connection': ['flix.subnets.6b2820d7-17c6-409a-91cb-b634cf596fdb'],
                    'segment': 'flix.vpcs.d48e294f-eb6a-4352-8d73-275b7a966e90',
                    'location': ['flix.dc.01'],
                    'address': '10.10.10.30'
                }
            }
        }

        # Run the conversion
        converted_data = convert(source_data)

        # Assert that the result is as expected
        self.assertEqual(converted_data, expected_output)

if __name__ == '__main__':
    unittest.main()
