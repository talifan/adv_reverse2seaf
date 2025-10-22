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
            },
            'seaf.ta.reverse.cloud_ru.advanced.subnets': {
                'flix.subnets.0d9f37b6-0889-4763-8cf3-20d9641af0c1': {
                    'id': '0d9f37b6-0889-4763-8cf3-20d9641af0c1',
                    'name': 'subnet-internal-1',
                    'cidr': '10.10.0.0/24'
                },
                'flix.subnets.1c9f37b6-0889-4763-8cf3-20d9641af0dd': {
                    'id': '1c9f37b6-0889-4763-8cf3-20d9641af0dd',
                    'name': 'subnet-internal-2',
                    'cidr': '10.10.10.0/24'
                },
                'flix.subnets.9c9f37b6-0889-4763-8cf3-20d9641af0ee': {
                    'id': '9c9f37b6-0889-4763-8cf3-20d9641af0ee',
                    'name': 'subnet-external',
                    'cidr': '10.1.5.0/24'
                },
                'flix.subnets.invalid-cidr': {
                    'id': 'invalid-cidr',
                    'name': 'broken',
                    'cidr': 'not-a-cidr'
                }
            },
            'seaf.ta.reverse.cloud_ru.advanced.ecss': {
                'flix.ecss.internal': {
                    'id': 'internal-ecs',
                    'name': 'ecs-internal',
                    'vpc_id': 'd48e294f-eb6a-4352-8d73-275b7a966e90',
                    'az': 'ru-moscow-1a',
                    'disks': [
                        {
                            'disk-1': {
                                'az': 'ru-moscow-1a'
                            }
                        }
                    ],
                    'DC': 'flix.dc.ru-moscow-1a'
                },
                'flix.ecss.external': {
                    'id': 'external-ecs',
                    'name': 'ecs-external',
                    'vpc_id': 'abddcd66-c607-4ec6-9d12-30378e0e54c0',
                    'az': 'ru-moscow-1b',
                    'disks': [],
                    'DC': 'flix.dc.ru-moscow-1b'
                }
            },
            'seaf.ta.reverse.cloud_ru.advanced.cces': {
                'flix.cces.cluster-01': {
                    'vpc_id': 'abddcd66-c607-4ec6-9d12-30378e0e54c0',
                    'masters_az': ['ru-moscow-1b']
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
                        'location': 'flix.dc.ru-moscow-1a',
                        'zone': '###PLACEHOLDER_FOR_MANUAL_ZONE###'
                    }
                },
                'flix.vpcs.abddcd66-c607-4ec6-9d12-30378e0e54c0': {
                    'title': 'vpc-external',
                    'description': 'CIDR: 10.1.0.0/16\nTenant: 9f7dcs8823ed23e9cwe223ecwe22236',
                    'external_id': 'abddcd66-c607-4ec6-9d12-30378e0e54c0',
                    'sber': {
                        'location': 'flix.dc.ru-moscow-1b',
                        'zone': '###PLACEHOLDER_FOR_MANUAL_ZONE###'
                    }
                }
            },
            'seaf.ta.components.network': {
                'flix.vpcs.d48e294f-eb6a-4352-8d73-275b7a966e90.router': {
                    'title': 'Маршрутизатор vpc-internal',
                    'description': 'Связанная VPC: vpc-internal\nCIDR: 10.10.0.0/16\nРасположение: flix.dc.ru-moscow-1a',
                    'external_id': 'd48e294f-eb6a-4352-8d73-275b7a966e90',
                    'model': 'Cloud Router',
                    'realization_type': 'Виртуальный',
                    'type': 'Маршрутизатор',
                    'network_connection': [
                        'flix.subnets.0d9f37b6-0889-4763-8cf3-20d9641af0c1',
                        'flix.subnets.1c9f37b6-0889-4763-8cf3-20d9641af0dd'
                    ],
                    'segment': 'flix.vpcs.d48e294f-eb6a-4352-8d73-275b7a966e90',
                    'location': ['flix.dc.ru-moscow-1a']
                },
                'flix.vpcs.abddcd66-c607-4ec6-9d12-30378e0e54c0.router': {
                    'title': 'Маршрутизатор vpc-external',
                    'description': 'Связанная VPC: vpc-external\nCIDR: 10.1.0.0/16\nРасположение: flix.dc.ru-moscow-1b',
                    'external_id': 'abddcd66-c607-4ec6-9d12-30378e0e54c0',
                    'model': 'Cloud Router',
                    'realization_type': 'Виртуальный',
                    'type': 'Маршрутизатор',
                    'network_connection': [
                        'flix.subnets.9c9f37b6-0889-4763-8cf3-20d9641af0ee'
                    ],
                    'segment': 'flix.vpcs.abddcd66-c607-4ec6-9d12-30378e0e54c0',
                    'location': ['flix.dc.ru-moscow-1b']
                }
            }
        }

        # Run the conversion
        converted_data = convert(source_data)

        # Assert that the result is as expected
        self.assertEqual(converted_data, expected_output)

if __name__ == '__main__':
    unittest.main()
