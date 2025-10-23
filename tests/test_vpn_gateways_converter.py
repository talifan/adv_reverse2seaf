import unittest
import sys
import os

# Add modules to the python path
sys.path.append(os.path.abspath('_metamodel_/iaas/converter/modules'))
sys.path.append(os.path.abspath('_metamodel_/iaas/converter/utils'))

from id_prefix import set_prefix
from vpn_gateways_converter import convert

set_prefix('tenant')

class TestVpnGatewaysConverter(unittest.TestCase):

    def test_convert_vpn_gateways(self):
        # Sample input data including Subnets and VPCs for linking
        source_data = {
            'seaf.ta.reverse.cloud_ru.advanced.vpcs': {
                'tenant.vpcs.abddcd66-c607-4ec6-9d12-30378e0e54c0': {
                    'id': 'abddcd66-c607-4ec6-9d12-30378e0e54c0',
                    'name': 'vpc-external'
                }
            },
            'seaf.ta.reverse.cloud_ru.advanced.subnets': {
                'tenant.subnets.fa768d9d-787e-4778-930d-8b8049f01df4': {
                    'id': 'fa768d9d-787e-4778-930d-8b8049f01df4',
                    'name': 'subnet-internet',
                    'cidr': '10.1.1.0/24',
                    'vpc': 'abddcd66-c607-4ec6-9d12-30378e0e54c0',
                    'availability_zone': 'ru-moscow-1a',
                    'DC': 'tenant.dc.ru-moscow-1a'
                }
            },
            'seaf.ta.reverse.cloud_ru.advanced.ecss': {
                'tenant.ecss.sample': {
                    'id': 'sample',
                    'name': 'ecs-sample',
                    'az': 'ru-moscow-1a',
                    'subnets': ['fa768d9d-787e-4778-930d-8b8049f01df4']
                }
            },
            'seaf.ta.reverse.cloud_ru.advanced.vpn_gateways': {
                'tenant.vpn_gateways.vpngw-offices': {
                    'id': 'vpngw-offices',
                    'name': 'vpngw-offices',
                    'vpc_id': 'abddcd66-c607-4ec6-9d12-30378e0e54c0',
                    'subnet_id': 'fa768d9d-787e-4778-930d-8b8049f01df4',
                    'ip_address': '188.72.107.53',
                    'type': 'IPSec',
                    'tenant': '9f7dcs8823ed23e9cwe223ecwe22236',
                    'DC': 'tenant.dc.01'
                }
            }
        }

        # Expected output
        expected_output = {
            'seaf.ta.components.network': {
                'tenant.vpn_gateways.vpngw-offices': {
                    'title': 'vpngw-offices',
                    'description': 'IP Address: 188.72.107.53\nProtocol: IPSec\nTenant: 9f7dcs8823ed23e9cwe223ecwe22236\nDC: tenant.dc.ru-moscow-1a',
                    'external_id': 'vpngw-offices',
                    'model': 'Cloud VPN Gateway',
                    'realization_type': 'Виртуальный',
                    'type': 'VPN',
                    'network_connection': ['tenant.subnets.fa768d9d-787e-4778-930d-8b8049f01df4'],
                    'segment': 'tenant.vpcs.abddcd66-c607-4ec6-9d12-30378e0e54c0',
                    'location': ['tenant.dc.ru-moscow-1a'],
                    'address': '188.72.107.53'
                }
            }
        }

        # Run the conversion
        converted_data = convert(source_data)

        # Assert that the result is as expected
        self.assertEqual(converted_data, expected_output)

if __name__ == '__main__':
    unittest.main()
