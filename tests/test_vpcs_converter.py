import unittest
import sys
import os

# Add modules to the python path
sys.path.append(os.path.abspath('modules'))

from vpcs_converter import convert

class TestVpcsConverter(unittest.TestCase):

    def test_convert_vpcs(self):
        # Sample input data mimicking the structure of the source YAML files
        source_data = {
            'seaf.ta.reverse.cloud_ru.advanced.vpcs': {
                'flix.vpcs.d48e294f-eb6a-4352-8d73-275b7a966e90': {
                    'id': 'd48e294f-eb6a-4352-8d73-275b7a966e90',
                    'name': 'vpc-internal',
                    'cidr': '10.10.0.0/16',
                    'description': 'Internal services VPC',
                    'tenant': '9f7dcs8823ed23e9cwe223ecwe22236',
                    'DC': 'flix.dc.01'
                },
                'flix.vpcs.abddcd66-c607-4ec6-9d12-30378e0e54c0': {
                    'id': 'abddcd66-c607-4ec6-9d12-30378e0e54c0',
                    'name': 'vpc-external',
                    'cidr': '10.1.0.0/16',
                    'description': '',
                    'tenant': '9f7dcs8823ed23e9cwe223ecwe22236',
                    'DC': 'flix.dc.01'
                }
            }
        }

        # Expected output after conversion
        expected_output = {
            'seaf.ta.services.network_segment': {
                'flix.vpcs.d48e294f-eb6a-4352-8d73-275b7a966e90': {
                    'title': 'vpc-internal',
                    'description': 'Internal services VPC\nCIDR: 10.10.0.0/16\nTenant: 9f7dcs8823ed23e9cwe223ecwe22236',
                    'external_id': 'd48e294f-eb6a-4352-8d73-275b7a966e90',
                    'sber': {
                        'location': 'flix.dc.01',
                        'zone': '###PLACEHOLDER_FOR_MANUAL_ZONE###'
                    }
                },
                'flix.vpcs.abddcd66-c607-4ec6-9d12-30378e0e54c0': {
                    'title': 'vpc-external',
                    'description': 'CIDR: 10.1.0.0/16\nTenant: 9f7dcs8823ed23e9cwe223ecwe22236',
                    'external_id': 'abddcd66-c607-4ec6-9d12-30378e0e54c0',
                    'sber': {
                        'location': 'flix.dc.01',
                        'zone': '###PLACEHOLDER_FOR_MANUAL_ZONE###'
                    }
                }
            }
        }

        # Run the conversion
        converted_data = convert(source_data)

        # Assert that the result is as expected
        self.assertEqual(converted_data, expected_output)

if __name__ == '__main__':
    unittest.main()
