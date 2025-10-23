import unittest
import sys
import os

# Add modules to the python path
sys.path.append(os.path.abspath('_metamodel_/iaas/converter/modules'))
sys.path.append(os.path.abspath('_metamodel_/iaas/converter/utils'))

from id_prefix import set_prefix
from peerings_converter import convert

set_prefix('tenant')

class TestPeeringsConverter(unittest.TestCase):

    def test_convert_peerings(self):
        # Sample input data including VPCs for linking
        source_data = {
            'seaf.ta.reverse.cloud_ru.advanced.vpcs': {
                'tenant.vpcs.d48e294f-eb6a-4352-8d73-275b7a966e90': {
                    'id': 'd48e294f-eb6a-4352-8d73-275b7a966e90',
                    'name': 'vpc-internal'
                },
                'tenant.vpcs.abddcd66-c607-4ec6-9d12-30378e0e54c0': {
                    'id': 'abddcd66-c607-4ec6-9d12-30378e0e54c0',
                    'name': 'vpc-external'
                }
            },
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
            'seaf.ta.services.logical_link': {
                'tenant.peerings.b58bce54-e2c9-4d00-b5eb-a7db6e80bd7c': {
                    'title': 'peering-Internal-External',
                    'description': 'VPC Peering between internal and external VPCs\nStatus: ACTIVE\nTenant: 9f7dcs8823ed23e9cwe223ecwe22236\nDC: tenant.dc.01',
                    'external_id': 'b58bce54-e2c9-4d00-b5eb-a7db6e80bd7c',
                    'source': 'tenant.vpcs.d48e294f-eb6a-4352-8d73-275b7a966e90',
                    'target': [
                        'tenant.vpcs.abddcd66-c607-4ec6-9d12-30378e0e54c0'
                    ],
                    'direction': '<==>',
                }
            }
        }

        # Run the conversion
        converted_data = convert(source_data)

        # Assert that the result is as expected
        self.assertEqual(converted_data, expected_output)

if __name__ == '__main__':
    unittest.main()
