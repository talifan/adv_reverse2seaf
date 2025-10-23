import unittest
import sys
import os

# Add modules to the python path
sys.path.append(os.path.abspath('_metamodel_/iaas/converter/modules'))
sys.path.append(os.path.abspath('_metamodel_/iaas/converter/utils'))

from id_prefix import set_prefix
from vpn_connections_converter import convert

set_prefix('tenant')

class TestVpnConnectionsConverter(unittest.TestCase):

    def test_convert_vpn_connections(self):
        # Sample input data including VPN Gateways, Offices, and DCs for linking
        source_data = {
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
            },
            'seaf.ta.reverse.cloud_ru.advanced.branches': {
                'tenant.branches.kremlin': {
                    'id': 'kremlin',
                    'name': 'Кремль',
                    'country': 'Россия',
                    'city': 'Москва',
                    'location': 'Красная площадь 1'
                },
                'tenant.branches.spb': {
                    'id': 'spb',
                    'name': 'Смольный',
                    'country': 'Россия',
                    'city': 'Санкт-Петербург',
                    'location': 'Смольный проезд 1'
                }
            },
            'seaf.ta.reverse.cloud_ru.advanced.vpn_connections': {
                'tenant.vpn_connections.vpn-hq': {
                    'id': 'vpn-hq',
                    'name': 'vpn-hq',
                    'gw_id': 'vpngw-offices',
                    'remote_gw_ip': '95.6.17.199',
                    'remote_subnets': ['10.1.0.0/21'],
                    'branch_id': 'tenant.office.hq', # This will be mapped to tenant.branches.kremlin or similar
                    'tenant': '9f7dcs8823ed23e9cwe223ecwe22236',
                    'DC': 'tenant.dc.01'
                },
                'tenant.vpn_connections.vpn-dc02': {
                    'id': 'vpn-dc02',
                    'name': 'vpn-dc02',
                    'gw_id': 'vpngw-offices',
                    'remote_gw_ip': '95.64.175.198',
                    'remote_subnets': ['172.16.0.0/16'],
                    'branch_id': 'tenant.dc.02', # This will be mapped to tenant.dc.02
                    'tenant': '9f7dcs8823ed23e9cwe223ecwe22236',
                    'DC': 'tenant.dc.01'
                }
            }
        }

        # Expected output
        expected_output = {
            'seaf.ta.services.logical_link': {
                'tenant.vpn_connections.vpn-hq': {
                    'title': 'vpn-hq',
                    'description': 'Remote Gateway IP: 95.6.17.199\nRemote Subnets: 10.1.0.0/21\nTenant: 9f7dcs8823ed23e9cwe223ecwe22236\nDC: tenant.dc.01',
                    'external_id': 'vpn-hq',
                    'source': 'tenant.vpn_gateways.vpngw-offices',
                    'target': [
                        'tenant.office.hq'
                    ],
                    'direction': '<==>',
                },
                'tenant.vpn_connections.vpn-dc02': {
                    'title': 'vpn-dc02',
                    'description': 'Remote Gateway IP: 95.64.175.198\nRemote Subnets: 172.16.0.0/16\nTenant: 9f7dcs8823ed23e9cwe223ecwe22236\nDC: tenant.dc.01',
                    'external_id': 'vpn-dc02',
                    'source': 'tenant.vpn_gateways.vpngw-offices',
                    'target': [
                        'tenant.dc.02'
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
