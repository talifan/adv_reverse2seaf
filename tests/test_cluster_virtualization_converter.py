import unittest
import sys
import os

# Add modules to the python path
sys.path.append(os.path.abspath('../modules'))

from id_prefix import set_prefix
from cluster_virtualization_converter import convert

set_prefix('tenant')

class TestClusterVirtualizationConverter(unittest.TestCase):

    def test_convert_cluster_virtualization(self):
        # Sample input data with various AZs and subnets from ECSs
        source_data = {
            'seaf.ta.reverse.cloud_ru.advanced.ecss': {
                'ecs1': {
                    'az': 'ru-moscow-1a',
                    'disks': [{'az': 'ru-moscow-1a'}, {'az': 'ru-moscow-1b'}],
                    'subnets': ['subnet-id-1', 'subnet-id-2']
                },
                'ecs2': {
                    'az': 'ru-moscow-1c',
                    'disks': [],
                    'subnets': ['subnet-id-2', 'subnet-id-3']
                }
            }
        }

        # Expected output
        expected_output = {
            'seaf.ta.services.cluster_virtualization': {
                'tenant.cluster_virtualization.cloud_ru_virtualization_cluster': {
                    'title': 'Cloud.ru Virtualization Cluster',
                    'external_id': 'cloud_ru_virtualization_cluster',
                    'hypervisor': 'Cloud.ru Hypervisor',
                    'availabilityzone': [
                        'tenant.dc_az.ru-moscow-1a',
                        'tenant.dc_az.ru-moscow-1b',
                        'tenant.dc_az.ru-moscow-1c'
                    ],
                    'location': [],
                    'network_connection': [
                        'tenant.subnets.subnet-id-1',
                        'tenant.subnets.subnet-id-2',
                        'tenant.subnets.subnet-id-3'
                    ],
                }
            }
        }

        # Run the conversion
        converted_data = convert(source_data)

        # Assert that the result is as expected
        self.assertEqual(converted_data, expected_output)

    def test_convert_cluster_virtualization_no_ecss(self):
        # Test case with no ECSs in source data
        source_data = {
            'seaf.ta.reverse.cloud_ru.advanced.ecss': {}
        }
        expected_output = {
            'seaf.ta.services.cluster_virtualization': {}
        }
        converted_data = convert(source_data)
        self.assertEqual(converted_data, expected_output)


if __name__ == '__main__':
    unittest.main()
