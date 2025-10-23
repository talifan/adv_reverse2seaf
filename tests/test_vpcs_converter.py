import unittest
import sys
import os

# Add modules to the python path
sys.path.append(os.path.abspath('modules'))

from id_prefix import set_prefix
from vpcs_converter import convert

set_prefix('tenant')

class TestVpcsConverter(unittest.TestCase):

    def test_convert_vpcs(self):
        # Sample input data mimicking the structure of the source YAML files
        source_data = {
            'seaf.ta.reverse.cloud_ru.advanced.vpcs': {
                'tenant.vpcs.d48e294f-eb6a-4352-8d73-275b7a966e90': {
                    'id': 'd48e294f-eb6a-4352-8d73-275b7a966e90',
                    'name': 'vpc-internal',
                    'cidr': '10.10.0.0/16',
                    'description': 'Internal services VPC',
                    'tenant': '9f7dcs8823ed23e9cwe223ecwe22236',
                    'DC': 'tenant.dc.01'
                },
                'tenant.vpcs.abddcd66-c607-4ec6-9d12-30378e0e54c0': {
                    'id': 'abddcd66-c607-4ec6-9d12-30378e0e54c0',
                    'name': 'vpc-external',
                    'cidr': '10.1.0.0/16',
                    'description': '',
                    'tenant': '9f7dcs8823ed23e9cwe223ecwe22236',
                    'DC': 'tenant.dc.01'
                }
            },
            'seaf.ta.reverse.cloud_ru.advanced.subnets': {
                'tenant.subnets.0d9f37b6-0889-4763-8cf3-20d9641af0c1': {
                    'id': '0d9f37b6-0889-4763-8cf3-20d9641af0c1',
                    'name': 'subnet-internal-1',
                    'cidr': '10.10.0.0/24'
                },
                'tenant.subnets.1c9f37b6-0889-4763-8cf3-20d9641af0dd': {
                    'id': '1c9f37b6-0889-4763-8cf3-20d9641af0dd',
                    'name': 'subnet-internal-2',
                    'cidr': '10.10.10.0/24'
                },
                'tenant.subnets.9c9f37b6-0889-4763-8cf3-20d9641af0ee': {
                    'id': '9c9f37b6-0889-4763-8cf3-20d9641af0ee',
                    'name': 'subnet-external',
                    'cidr': '10.1.5.0/24'
                },
                'tenant.subnets.invalid-cidr': {
                    'id': 'invalid-cidr',
                    'name': 'broken',
                    'cidr': 'not-a-cidr'
                }
            },
            'seaf.ta.reverse.cloud_ru.advanced.ecss': {
                'tenant.ecss.internal': {
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
                    'DC': 'tenant.dc.ru-moscow-1a'
                },
                'tenant.ecss.external': {
                    'id': 'external-ecs',
                    'name': 'ecs-external',
                    'vpc_id': 'abddcd66-c607-4ec6-9d12-30378e0e54c0',
                    'az': 'ru-moscow-1b',
                    'disks': [],
                    'DC': 'tenant.dc.ru-moscow-1b'
                }
            },
            'seaf.ta.reverse.cloud_ru.advanced.cces': {
                'tenant.cces.cluster-01': {
                    'vpc_id': 'abddcd66-c607-4ec6-9d12-30378e0e54c0',
                    'masters_az': ['ru-moscow-1b']
                }
            }
        }

        # Expected output after conversion
        expected_output = {
            'seaf.ta.services.network_segment': {
                'tenant.vpcs.d48e294f-eb6a-4352-8d73-275b7a966e90': {
                    'title': 'vpc-internal',
                    'description': 'Internal services VPC\nCIDR: 10.10.0.0/16\nTenant: 9f7dcs8823ed23e9cwe223ecwe22236',
                    'external_id': 'd48e294f-eb6a-4352-8d73-275b7a966e90',
                    'sber': {
                        'location': 'tenant.dc.ru-moscow-1a',
                        'zone': '###PLACEHOLDER_FOR_MANUAL_ZONE###'
                    }
                },
                'tenant.vpcs.abddcd66-c607-4ec6-9d12-30378e0e54c0': {
                    'title': 'vpc-external',
                    'description': 'CIDR: 10.1.0.0/16\nTenant: 9f7dcs8823ed23e9cwe223ecwe22236',
                    'external_id': 'abddcd66-c607-4ec6-9d12-30378e0e54c0',
                    'sber': {
                        'location': 'tenant.dc.ru-moscow-1b',
                        'zone': '###PLACEHOLDER_FOR_MANUAL_ZONE###'
                    }
                }
            },
            'seaf.ta.components.network': {
                'tenant.vpcs.d48e294f-eb6a-4352-8d73-275b7a966e90.router': {
                    'title': 'Маршрутизатор vpc-internal',
                    'description': 'Связанная VPC: vpc-internal\nCIDR: 10.10.0.0/16\nРасположение: tenant.dc.ru-moscow-1a',
                    'external_id': 'd48e294f-eb6a-4352-8d73-275b7a966e90',
                    'model': 'Cloud Router',
                    'realization_type': 'Виртуальный',
                    'type': 'Маршрутизатор',
                    'network_connection': [
                        'tenant.subnets.0d9f37b6-0889-4763-8cf3-20d9641af0c1',
                        'tenant.subnets.1c9f37b6-0889-4763-8cf3-20d9641af0dd'
                    ],
                    'segment': 'tenant.vpcs.d48e294f-eb6a-4352-8d73-275b7a966e90',
                    'location': ['tenant.dc.ru-moscow-1a']
                },
                'tenant.vpcs.abddcd66-c607-4ec6-9d12-30378e0e54c0.router': {
                    'title': 'Маршрутизатор vpc-external',
                    'description': 'Связанная VPC: vpc-external\nCIDR: 10.1.0.0/16\nРасположение: tenant.dc.ru-moscow-1b',
                    'external_id': 'abddcd66-c607-4ec6-9d12-30378e0e54c0',
                    'model': 'Cloud Router',
                    'realization_type': 'Виртуальный',
                    'type': 'Маршрутизатор',
                    'network_connection': [
                        'tenant.subnets.9c9f37b6-0889-4763-8cf3-20d9641af0ee'
                    ],
                    'segment': 'tenant.vpcs.abddcd66-c607-4ec6-9d12-30378e0e54c0',
                    'location': ['tenant.dc.ru-moscow-1b']
                }
            }
        }

        # Run the conversion
        converted_data = convert(source_data)

        # Assert that the result is as expected
        self.assertEqual(converted_data, expected_output)

if __name__ == '__main__':
    unittest.main()
