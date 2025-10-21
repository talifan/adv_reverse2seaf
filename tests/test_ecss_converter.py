import unittest
import sys
import os

# Add modules to the python path
sys.path.append(os.path.abspath('_metamodel_/iaas/converter/modules'))

from ecss_converter import convert

class TestEcssConverter(unittest.TestCase):

    def test_convert_ecss(self):
        # Sample input data including VPCs and Subnets for linking
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
                    'cidr': '10.10.0.0/24',
                    'vpc': 'd48e294f-eb6a-4352-8d73-275b7a966e90'
                }
            },
            'seaf.ta.reverse.cloud_ru.advanced.ecss': {
                'flix.ecss.e5e60a69-0653-4297-8799-ea0df4f0cacc': {
                    'id': 'e5e60a69-0653-4297-8799-ea0df4f0cacc',
                    'name': 'ecs-prod-someserver1',
                    'flavor': 's7n.large.2',
                    'os': {
                        'type': 'Linux',
                        'bit': '64'
                    },
                    'vpc_id': 'd48e294f-eb6a-4352-8d73-275b7a966e90',
                    'az': 'ru-moscow-1a',
                    'cpu': {
                        'cores': 2,
                        'frequency': '2500' # String in source, int in target
                    },
                    'ram': 4096, # MB in source, GB in target
                    'nic_qty': 1,
                    'addresses': ['10.10.0.51'],
                    'subnets': ['0d9f37b6-0889-4763-8cf3-20d9641af0c1'],
                    'disks': [
                        {
                            'device': '/dev/vda',
                            'size': '50', # String in source, int in target
                            'az': 'ru-moscow-1a',
                            'type': 'SAS'
                        }
                    ],
                    'tags': [
                        {'key': 'AS_Name', 'value': 'SomewhatAS'},
                        {'key': 'Service_Name', 'value': 'Application Server'}
                    ],
                    'security_groups': ['0fdb3e4f-c7a6-42eb-9531-552ac5006202'],
                    'type': 'vm',
                    'tenant': '9f7dcs8823ed23e9cwe223ecwe22236',
                    'DC': 'flix.dc.01',
                    'description': 'Example server description'
                }
            }
        }

        # Expected output
        expected_output = {
            'seaf.ta.components.server': {
                'flix.ecss.e5e60a69-0653-4297-8799-ea0df4f0cacc': {
                    'title': 'ecs-prod-someserver1',
                    'description': 'Example server description\nFlavor: s7n.large.2\nIP Addresses: 10.10.0.51\nSecurity Groups: 0fdb3e4f-c7a6-42eb-9531-552ac5006202\nTags: AS_Name:SomewhatAS, Service_Name:Application Server\nTenant: 9f7dcs8823ed23e9cwe223ecwe22236\nDC: flix.dc.01',
                    'external_id': 'e5e60a69-0653-4297-8799-ea0df4f0cacc',
                    'type': 'Виртуальный',
                    'fqdn': 'ecs-prod-someserver1',
                    'os': {
                        'type': 'Linux',
                        'bit': '64'
                    },
                    'cpu': {
                        'cores': 2,
                        'frequency': 2500
                    },
                    'ram': 4, # 4096 MB / 1024 = 4 GB
                    'nic_qty': 1,
                    'disks': [
                        {
                            'az': 'flix.dc_az.ru-moscow-1a',
                            'size': 50,
                            'type': 'SAS',
                            'device': '/dev/vda'
                        }
                    ],
                    'az': ['flix.dc_az.ru-moscow-1a'],
                    'subnets': ['flix.subnets.0d9f37b6-0889-4763-8cf3-20d9641af0c1'],
                    'virtualization': 'flix.cluster_virtualization.cloud_ru_virtualization_cluster'
                }
            }
        }

        # Run the conversion
        converted_data = convert(source_data)

        # Assert that the result is as expected
        self.assertEqual(converted_data, expected_output)

if __name__ == '__main__':
    unittest.main()
