import unittest
import sys
import os

# Add modules to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))

from id_prefix import set_prefix
from id_prefix import set_prefix
from peerings_converter import convert

class TestPeeringsConverter(unittest.TestCase):

    def test_convert_peerings(self):
        set_prefix('tenant')
        # Sample input data
        source_data = {
            'seaf.ta.reverse.cloud_ru.advanced.peerings': {
                'tenant.peerings.b58bce54-e2c9-4d00-b5eb-a7db6e80bd7c': {
                    'id': 'b58bce54-e2c9-4d00-b5eb-a7db6e80bd7c',
                    'name': 'peering-Internal-External',
                    'request_vpc': 'd48e294f-eb6a-4352-8d73-275b7a966e90',
                    'accept_vpc': 'abddcd66-c607-4ec6-9d12-30378e0e54c0',
                    'description': 'VPC Peering between internal and external VPCs',
                    'status': 'ACTIVE',
                    'tenant': '9f7dcs8823ed23e9cwe223ecwe22236',
                    'DC': 'tenant.dc.01'
                }
            }
        }

        # Expected output
        expected_output = {
            'seaf.ta.services.network_links': {
                'tenant.peerings.b58bce54-e2c9-4d00-b5eb-a7db6e80bd7c': {
                    'title': 'peering-Internal-External',
                    'description': 'VPC Peering between internal and external VPCs\nStatus: ACTIVE\nTenant: 9f7dcs8823ed23e9cwe223ecwe22236\nDC: tenant.dc.01',
                    'external_id': 'b58bce54-e2c9-4d00-b5eb-a7db6e80bd7c',
                    'network_connection': [
                        'tenant.vpcs.d48e294f-eb6a-4352-8d73-275b7a966e90.router',
                        'tenant.vpcs.abddcd66-c607-4ec6-9d12-30378e0e54c0.router'
                    ],
                    'technology': 'VPC Peering'
                }
            }
        }

        # Run the conversion
        converted_data = convert(source_data)

        # Assert that the result is as expected
        self.assertEqual(converted_data, expected_output)

if __name__ == '__main__':
    unittest.main()
