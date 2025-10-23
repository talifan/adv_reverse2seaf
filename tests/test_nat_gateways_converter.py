import unittest
import sys
import os
import json

# Add modules to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))

from id_prefix import set_prefix, segment_ref
from id_prefix import set_prefix, segment_ref
from nat_gateways_converter import convert

class TestNatGatewaysConverter(unittest.TestCase):

    def test_convert_nat_gateways(self):
        set_prefix('tenant')
        # Sample input data including Subnets for linking
        source_data = {
            'seaf.ta.reverse.cloud_ru.advanced.subnets': {
                'tenant.subnets.0d9f37b6-0889-4763-8cf3-20d9641af0c1': {
                    'id': '0d9f37b6-0889-4763-8cf3-20d9641af0c1',
                    'name': 'subnet-Prod',
                    'cidr': '10.10.0.0/24',
                    'vpc': 'd48e294f-eb6a-4352-8d73-275b7a966e90',
                    'availability_zone': 'ru-moscow-1c',
                    'DC': 'tenant.dc.ru-moscow-1c'
                }
            },
            'seaf.ta.reverse.cloud_ru.advanced.nat_gateways': {
                'tenant.nat_gateways.d9dade58-8b2c-4505-814f-eb38e503f1b1': {
                    'id': 'd9dade58-8b2c-4505-814f-eb38e503f1b1',
                    'name': 'nat-gateway',
                    'description': 'Main NAT Gateway',
                    'subnet_id': '0d9f37b6-0889-4763-8cf3-20d9641af0c1',
                    'tenant': '9f7dcs8823ed23e9cwe223ecwe22236',
                    'DC': 'tenant.dc.01',
                    'status': 'ACTIVE',
                    'address': '10.10.0.25',
                    'snat_rules': [
                        {
                            'id': '00c4fa69-38f5-4df7-88fd-f98ae315db51',
                            'eip_id': ['7785b143-e83f-4466-aa22-05b2419fc670'],
                            'eip_address': ['170.170.190.235'],
                            'status': 'ACTIVE',
                            'subnet_id': '0d9f37b6-0889-4763-8cf3-20d9641af0c1',
                            'cidr': '',
                            'source_type': 0
                        }
                    ],
                    'dnat_rules': []
                }
            },
            'seaf.ta.reverse.cloud_ru.advanced.ecss': {}
        }

        # Expected output
        expected_output = {
            'seaf.ta.components.network': {
                'tenant.nat_gateways.d9dade58-8b2c-4505-814f-eb38e503f1b1': {
                    'title': 'nat-gateway',
                    'description': 'Main NAT Gateway\nInternal IP: 10.10.0.25\nStatus: ACTIVE\nTenant: 9f7dcs8823ed23e9cwe223ecwe22236\nSNAT Rules: ' + json.dumps([
                        {
                            'id': '00c4fa69-38f5-4df7-88fd-f98ae315db51',
                            'eip_id': ['7785b143-e83f-4466-aa22-05b2419fc670'],
                            'eip_address': ['170.170.190.235'],
                            'status': 'ACTIVE',
                            'subnet_id': '0d9f37b6-0889-4763-8cf3-20d9641af0c1',
                            'cidr': '',
                            'source_type': 0
                        }
                    ], indent=2) + '\nDNAT Rules: []\nDC: tenant.dc.ru-moscow-1c',
                    'external_id': 'd9dade58-8b2c-4505-814f-eb38e503f1b1',
                    'model': 'Cloud NAT Gateway',
                    'realization_type': 'Виртуальный',
                    'type': 'NAT',
                    'network_connection': ['tenant.subnets.0d9f37b6-0889-4763-8cf3-20d9641af0c1'],
                    'segment': 'tenant.segment.ru-moscow-1c.INT-NET',
                    'location': ['tenant.dc.ru-moscow-1c'],
                    'address': '10.10.0.25'
                }
            }
        }

        # Run the conversion
        converted_data = convert(source_data)

        # Assert that the result is as expected
        self.assertEqual(converted_data, expected_output)

if __name__ == '__main__':
    unittest.main()
