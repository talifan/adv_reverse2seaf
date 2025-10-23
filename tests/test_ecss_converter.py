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
                            'disk-uuid-1': {
                                'device': '/dev/vda',
                                'size': '50', # String in source, int in target
                                'az': 'ru-moscow-1a',
                                'type': 'SAS'
                            }
                        }
                    ],
                    'tags': [
                        {'key': 'AS_Name', 'value': 'SomewhatAS'},
                        {'key': 'Service_Name', 'value': 'Application Server'},
                        'system: example.systems.1c.example.com'
                    ],
                    'security_groups': ['0fdb3e4f-c7a6-42eb-9531-552ac5006202'],
                    'type': 'vm',
                    'tenant': '9f7dcs8823ed23e9cwe223ecwe22236',
                    'DC': 'flix.dc.01',
                    'description': 'Example server description'
                },
                'flix.ecss.test-server-units': {
                    'id': 'test-server-units',
                    'name': 'ecs-test-units',
                    'os': {
                        'type': 'Windows'
                    },
                    'cpu': {
                        'cores': 4,
                        'frequency': '3000 MHz'
                    },
                    'ram': 8192,
                    'disks': [
                        {
                            'disk-uuid-2': {
                                'device': '/dev/vda',
                                'size': '100 GB',
                                'type': 'SSD'
                            }
                        }
                    ],
                    'az': 'ru-moscow-1b',
                    'subnets': ['0d9f37b6-0889-4763-8cf3-20d9641af0c1']
                },
                'flix.ecss.test-server-float': {
                    'id': 'test-server-float',
                    'name': 'ecs-test-float',
                    'cpu': {
                        'frequency': '2.5GHz'
                    },
                    'disks': [
                        {
                            'disk-uuid-3': {
                                'device': '/dev/vdb',
                                'size': '120.5GB',
                                'type': 'NVMe'
                            }
                        }
                    ],
                },
                'flix.ecss.test-server-single-disk': {
                    'id': 'test-server-single-disk',
                    'name': 'ecs-test-single-disk',
                    'disks': [
                        {
                            'disk-uuid-4': {
                                'device': '/dev/vdc',
                                'size': 200,
                                'type': 'HDD'
                            }
                        }
                    ]
                }
            }
        }

        # Expected output
        expected_output = {
            'seaf.ta.components.server': {
                'flix.ecss.e5e60a69-0653-4297-8799-ea0df4f0cacc': {
                    'title': 'ecs-prod-someserver1',
                    'description': 'Example server description\nFlavor: s7n.large.2\nIP Addresses: 10.10.0.51\nSecurity Groups: 0fdb3e4f-c7a6-42eb-9531-552ac5006202\nTags: AS_Name:SomewhatAS, Service_Name:Application Server, system: example.systems.1c.example.com\nTenant: 9f7dcs8823ed23e9cwe223ecwe22236\nDC: flix.dc.01',
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
                    'location': ['flix.dc.ru-moscow-1a'],
                    'subnets': ['flix.subnets.0d9f37b6-0889-4763-8cf3-20d9641af0c1'],
                    'virtualization': 'flix.cluster_virtualization.cloud_ru_virtualization_cluster'
                },
                'flix.ecss.test-server-units': {
                    'title': 'ecs-test-units',
                    'description': '',
                    'external_id': 'test-server-units',
                    'type': 'Виртуальный',
                    'fqdn': 'ecs-test-units',
                    'os': {
                        'type': 'Windows',
                        'bit': None
                    },
                    'cpu': {
                        'cores': 4,
                        'frequency': 3000
                    },
                    'ram': 8,
                    'nic_qty': None,
                    'disks': [
                        {
                            'az': None,
                            'size': 100,
                            'type': 'SSD',
                            'device': '/dev/vda'
                        }
                    ],
                    'az': ['flix.dc_az.ru-moscow-1b'],
                    'location': ['flix.dc.ru-moscow-1b'],
                    'subnets': ['flix.subnets.0d9f37b6-0889-4763-8cf3-20d9641af0c1'],
                    'virtualization': 'flix.cluster_virtualization.cloud_ru_virtualization_cluster'
                },
                'flix.ecss.test-server-float': {
                    'title': 'ecs-test-float',
                    'description': '',
                    'external_id': 'test-server-float',
                    'type': 'Виртуальный',
                    'fqdn': 'ecs-test-float',
                    'os': {
                        'type': None,
                        'bit': None
                    },
                    'cpu': {
                        'cores': None,
                        'frequency': 2
                    },
                    'ram': 0,
                    'nic_qty': None,
                    'disks': [
                        {
                            'az': None,
                            'size': 120,
                            'type': 'NVMe',
                            'device': '/dev/vdb'
                        }
                    ],
                    'az': [],
                    'location': [],
                    'subnets': [],
                    'virtualization': 'flix.cluster_virtualization.cloud_ru_virtualization_cluster'
                },
                'flix.ecss.test-server-single-disk': {
                    'title': 'ecs-test-single-disk',
                    'description': '',
                    'external_id': 'test-server-single-disk',
                    'type': 'Виртуальный',
                    'fqdn': 'ecs-test-single-disk',
                    'os': {
                        'type': None,
                        'bit': None
                    },
                    'cpu': {
                        'cores': None,
                        'frequency': 0
                    },
                    'ram': 0,
                    'nic_qty': None,
                    'disks': [
                        {
                            'az': None,
                            'size': 200,
                            'type': 'HDD',
                            'device': '/dev/vdc'
                        }
                    ],
                    'az': [],
                    'location': [],
                    'subnets': [],
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
