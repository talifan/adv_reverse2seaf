import unittest
import sys
import os

# Add modules to the python path
sys.path.append(os.path.abspath('modules'))

from id_prefix import set_prefix
from subnets_converter import convert

set_prefix('tenant')

class TestSubnetsConverter(unittest.TestCase):

    def test_convert_subnets(self):
        # Sample input data including VPCs for linking
        source_data = {
            'seaf.ta.reverse.cloud_ru.advanced.vpcs': {
                'tenant.vpcs.d48e294f-eb6a-4352-8d73-275b7a966e90': {
                    'id': 'd48e294f-eb6a-4352-8d73-275b7a966e90',
                    'name': 'vpc-internal'
                }
            },
            'seaf.ta.reverse.cloud_ru.advanced.subnets': {
                'tenant.subnets.0d9f37b6-0889-4763-8cf3-20d9641af0c1': {
                    'id': '0d9f37b6-0889-4763-8cf3-20d9641af0c1',
                    'name': 'subnet-Prod',
                    'cidr': '10.10.0.0/24',
                    'description': 'Production network',
                    'gateway': '10.10.0.1',
                    'dns_list': ['100.1.3.5', '100.2.6.4'],
                    'vpc': 'd48e294f-eb6a-4352-8d73-275b7a966e90',
                    'tenant': '9f7dcs8823ed23e9cwe223ecwe22236',
                    'DC': 'tenant.dc.01'
                }
            }
        }

        # Expected output
        expected_output = {
            'seaf.ta.services.network': {
                'tenant.subnets.0d9f37b6-0889-4763-8cf3-20d9641af0c1': {
                    'title': 'subnet-Prod',
                    'description': 'Production network\nGateway: 10.10.0.1\nDNS: 100.1.3.5, 100.2.6.4\nTenant: 9f7dcs8823ed23e9cwe223ecwe22236',
                    'external_id': '0d9f37b6-0889-4763-8cf3-20d9641af0c1',
                    'type': 'LAN',
                    'ipnetwork': '10.10.0.0/24',
                    'segment': ['tenant.vpcs.d48e294f-eb6a-4352-8d73-275b7a966e90'],
                    'lan_type': 'Проводная'
                }
            }
        }

        # Run the conversion
        converted_data = convert(source_data)

        # Assert that the result is as expected
        self.assertEqual(converted_data, expected_output)

if __name__ == '__main__':
    unittest.main()