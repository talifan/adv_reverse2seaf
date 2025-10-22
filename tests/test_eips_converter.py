import unittest
import sys
import os

# Add modules to the python path
sys.path.append(os.path.abspath('_metamodel_/iaas/converter/modules'))

from eips_converter import convert

class TestEipsConverter(unittest.TestCase):

    def test_convert_eips(self):
        # Sample input data for EIPs, including subnets and vpcs for segment lookup
        source_data = {
            'seaf.ta.reverse.cloud_ru.advanced.vpcs': {
                'flix.vpcs.d48e294f-eb6a-4352-8d73-275b7a966e90': {
                    'id': 'd48e294f-eb6a-4352-8d73-275b7a966e90',
                    'name': 'vpc-internal'
                }
            },
            'seaf.ta.reverse.cloud_ru.advanced.subnets': {
                'flix.subnets.0d9f37b6-0889-4763-8cf3-20d9641af0c1': {
                    'id': '0d9f37b6-0889-4763-8cf3-20d9641af0c1',
                    'name': 'subnet-Prod',
                    'cidr': '10.1.1.0/24',
                    'vpc': 'd48e294f-eb6a-4352-8d73-275b7a966e90'
                }
            },
            'seaf.ta.reverse.cloud_ru.advanced.eips': {
                'flix.eips.37ee7c4f-75b8-45be-b6f4-42df28771e87': {
                    'id': '37ee7c4f-75b8-45be-b6f4-42df28771e87',
                    'type': '5_bgp',
                    'port_id': '964279e7-a83a-4555-a944-e357699a1b10',
                    'ext_address': '73.54.34.19',
                    'int_address': '10.1.1.3',
                    'limit': {
                        'type': 'WHOLE',
                        'throughput': 20,
                        'rule_id': 'ab899959-fe54-4e9d-9795-00d1034e318e',
                        'rule_name': 'bandwidth-online'
                    },
                    'tenant': '9f7dcs8823ed23e9cwe223ecwe22236',
                    'DC': 'flix.dc.01'
                }
            }
        }

        # Expected output
        expected_output = {
            'seaf.ta.services.network': {
                'flix.eips.37ee7c4f-75b8-45be-b6f4-42df28771e87': {
                    'title': '73.54.34.19',
                    'description': 'Internal IP: 10.1.1.3\nAddress Type: 5_bgp\nPort ID: 964279e7-a83a-4555-a944-e357699a1b10\nLimit Rule ID: ab899959-fe54-4e9d-9795-00d1034e318e\nLimit Rule Name: bandwidth-online\nLimit Throughput (Mbps): 20\nLimit Type: WHOLE\nTenant: 9f7dcs8823ed23e9cwe223ecwe22236\nDC: flix.dc.01',
                    'external_id': '37ee7c4f-75b8-45be-b6f4-42df28771e87',
                    'type': 'WAN',
                    'wan_ip': '73.54.34.19',
                    'segment': 'flix.vpcs.d48e294f-eb6a-4352-8d73-275b7a966e90',
                    'location': ['flix.dc.01'],
                    'provider': 'Cloud.ru'
                }
            }
        }

        # Run the conversion
        converted_data = convert(source_data)

        # Assert that the result is as expected
        self.assertEqual(converted_data, expected_output)

if __name__ == '__main__':
    unittest.main()
