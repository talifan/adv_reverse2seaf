import unittest
import sys
import os

# Add modules to the python path
sys.path.append(os.path.abspath('_metamodel_/iaas/converter/modules'))

from eips_converter import convert

class TestEipsConverter(unittest.TestCase):

    def test_convert_eips_with_public_and_private(self):
        # Sample input data for EIPs, including subnets and vpcs for segment lookup
        source_data = {
            'seaf.ta.reverse.cloud_ru.advanced.vpcs': {
                'flix.vpcs.vpc-internal-id': {
                    'id': 'vpc-internal-id',
                    'name': 'vpc-internal'
                }
            },
            'seaf.ta.reverse.cloud_ru.advanced.subnets': {
                'flix.subnets.subnet-prod-id': {
                    'id': 'subnet-prod-id',
                    'name': 'subnet-Prod',
                    'cidr': '10.1.1.0/24',
                    'vpc': 'vpc-internal-id'
                }
            },
            'seaf.ta.reverse.cloud_ru.advanced.ecss': {
                'flix.ecss.server-1': {
                    'id': 'server-1',
                    'name': 'ecs-server-1',
                    'addresses': ['10.1.1.4'],
                    'subnets': ['subnet-prod-id']
                }
            },
            'seaf.ta.reverse.cloud_ru.advanced.nat_gateways': {
                'flix.nat_gateways.nat-1': {
                    'id': 'nat-1',
                    'name': 'nat-gateway-1',
                    'address': '10.1.1.3'
                }
            },
            'seaf.ta.reverse.cloud_ru.advanced.eips': {
                # This EIP has a public ext_address, should be linked to the Internet segment
                'flix.eips.public-eip-id': {
                    'id': 'public-eip-id',
                    'ext_address': '8.8.8.8', # Public IP
                    'int_address': '10.1.1.3',
                    'tenant': 'tenant-a',
                    'DC': 'flix.dc.01'
                },
                # This EIP has a private ext_address, should use the regular segment lookup
                'flix.eips.private-eip-id': {
                    'id': 'private-eip-id',
                    'ext_address': '192.168.1.100', # Private IP
                    'int_address': '10.1.1.4',
                    'tenant': 'tenant-b',
                    'DC': 'flix.dc.01'
                }
            }
        }

        # Expected output
        expected_output = {
            'seaf.ta.services.network': {
                'flix.eips.public-eip-id': {
                    'title': '8.8.8.8',
                    'description': 'Internal IP: 10.1.1.3\nTenant: tenant-a\nDC: flix.dc.01',
                    'external_id': 'public-eip-id',
                    'type': 'WAN',
                    'wan_ip': '8.8.8.8',
                    'segment': 'flix.network_segment.internet', # Should point to internet
                    'location': ['flix.dc.01'],
                    'provider': 'Cloud.ru'
                },
                'flix.eips.private-eip-id': {
                    'title': '192.168.1.100',
                    'description': 'Internal IP: 10.1.1.4\nTenant: tenant-b\nDC: flix.dc.01',
                    'external_id': 'private-eip-id',
                    'type': 'WAN',
                    'wan_ip': '192.168.1.100',
                    'segment': 'flix.vpcs.vpc-internal-id', # Should use the regular lookup
                    'location': ['flix.dc.01'],
                    'provider': 'Cloud.ru'
                }
            },
            'seaf.ta.services.network_segment': {
                'flix.network_segment.internet': {
                    'title': 'Public Internet',
                    'description': 'Logical segment for all public-facing IP addresses.',
                    'external_id': 'internet_segment',
                    'sber': {
                        'zone': 'INTERNET'
                    }
                }
            },
            'seaf.ta.services.network_links': {
                'flix.eips.public-eip-id.link': {
                    'title': 'Связь EIP 8.8.8.8',
                    'description': 'EIP 8.8.8.8 связан с: flix.nat_gateways.nat-1',
                    'external_id': 'public-eip-id-link',
                    'network_connection': ['flix.eips.public-eip-id', 'flix.nat_gateways.nat-1'],
                    'technology': 'EIP'
                },
                'flix.eips.private-eip-id.link': {
                    'title': 'Связь EIP 192.168.1.100',
                    'description': 'EIP 192.168.1.100 связан с: flix.ecss.server-1',
                    'external_id': 'private-eip-id-link',
                    'network_connection': ['flix.eips.private-eip-id', 'flix.ecss.server-1'],
                    'technology': 'EIP'
                }
            }
        }

        # Run the conversion
        converted_data = convert(source_data)

        # Assert that the result is as expected
        self.assertEqual(converted_data, expected_output)

if __name__ == '__main__':
    unittest.main()
