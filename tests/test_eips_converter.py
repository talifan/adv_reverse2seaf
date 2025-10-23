import unittest
import sys
import os

# Add modules to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))

from id_prefix import set_prefix, segment_ref
from id_prefix import set_prefix, segment_ref
from eips_converter import convert

class TestEipsConverter(unittest.TestCase):

    def test_convert_eips_with_public_and_private(self):
        set_prefix('tenant')
        # Sample input data for EIPs, including subnets for AZ lookup
        source_data = {
            'seaf.ta.reverse.cloud_ru.advanced.subnets': {
                'tenant.subnets.subnet-prod-id': {
                    'id': 'subnet-prod-id',
                    'name': 'subnet-Prod',
                    'cidr': '10.1.1.0/24',
                    'vpc': 'vpc-internal-id',
                    'availability_zone': 'ru-moscow-1a'
                }
            },
            'seaf.ta.reverse.cloud_ru.advanced.ecss': {
                'tenant.ecss.server-1': {
                    'id': 'server-1',
                    'name': 'ecs-server-1',
                    'addresses': ['10.1.1.4'],
                    'subnets': ['subnet-prod-id']
                }
            },
            'seaf.ta.reverse.cloud_ru.advanced.nat_gateways': {
                'tenant.nat_gateways.nat-1': {
                    'id': 'nat-1',
                    'name': 'nat-gateway-1',
                    'address': '10.1.1.3'
                }
            },
            'seaf.ta.reverse.cloud_ru.advanced.elbs': {},
            'seaf.ta.reverse.cloud_ru.advanced.eips': {
                # This EIP has a public ext_address, should be linked to the INTERNET segment
                'tenant.eips.public-eip-id': {
                    'id': 'public-eip-id',
                    'ext_address': '8.8.8.8', # Public IP
                    'int_address': '10.1.1.3',
                    'tenant': 'tenant-a',
                    'DC': 'tenant.dc.01'
                },
                # This EIP has a private ext_address, should be linked to the INT-NET segment
                'tenant.eips.private-eip-id': {
                    'id': 'private-eip-id',
                    'ext_address': '192.168.1.100', # Private IP
                    'int_address': '10.1.1.4',
                    'tenant': 'tenant-b',
                    'DC': 'tenant.dc.01'
                }
            }
        }

        # Expected output
        expected_output = {
            'seaf.ta.services.network': {
                'tenant.eips.public-eip-id': {
                    'title': '8.8.8.8',
                    'description': 'Internal IP: 10.1.1.3\nTenant: tenant-a\nDC: tenant.dc.01',
                    'external_id': 'public-eip-id',
                    'type': 'WAN',
                    'wan_ip': '8.8.8.8',
                    'segment': ['tenant.segment.ru-moscow-1a.INTERNET'],
                    'provider': 'Cloud.ru'
                },
                'tenant.eips.private-eip-id': {
                    'title': '192.168.1.100',
                    'description': 'Internal IP: 10.1.1.4\nTenant: tenant-b\nDC: tenant.dc.01',
                    'external_id': 'private-eip-id',
                    'type': 'WAN',
                    'wan_ip': '192.168.1.100',
                    'segment': ['tenant.segment.ru-moscow-1a.INT-NET'],
                    'provider': 'Cloud.ru'
                }
            },
            'seaf.ta.services.network_links': {
                'tenant.eips.public-eip-id.link': {
                    'title': 'Связь EIP 8.8.8.8',
                    'description': 'EIP 8.8.8.8 связан с: tenant.nat_gateways.nat-1',
                    'external_id': 'public-eip-id-link',
                    'network_connection': ['tenant.eips.public-eip-id', 'tenant.nat_gateways.nat-1'],
                    'technology': 'EIP'
                },
                'tenant.eips.private-eip-id.link': {
                    'title': 'Связь EIP 192.168.1.100',
                    'description': 'EIP 192.168.1.100 связан с: tenant.ecss.server-1',
                    'external_id': 'private-eip-id-link',
                    'network_connection': ['tenant.eips.private-eip-id', 'tenant.ecss.server-1'],
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
