import unittest
import sys
import os

# Add modules to the python path
sys.path.append(os.path.abspath('../modules'))

from dc_az_converter import convert

class TestDCAZConverter(unittest.TestCase):

    def test_convert_dc_azs(self):
        # Sample input data with various AZs from different source entities
        source_data = {
            'seaf.ta.reverse.cloud_ru.advanced.ecss': {
                'ecs1': {'az': 'ru-moscow-1a', 'disks': [{'az': 'ru-moscow-1a'}, {'az': 'ru-moscow-1b'}]},
                'ecs2': {'az': 'ru-moscow-1c', 'disks': []}
            },
            'seaf.ta.reverse.cloud_ru.advanced.cces': {
                'cce1': {'masters_az': ['ru-moscow-1a', 'ru-moscow-1d']},
                'cce2': {'masters_az': []}
            },
            'seaf.ta.reverse.cloud_ru.advanced.rdss': {
                'rds1': {'az': ['ru-moscow-1b', 'ru-moscow-1e']},
                'rds2': {'az': []}
            },
            'seaf.ta.reverse.cloud_ru.advanced.dmss': {
                'dms1': {'available_az': ['ru-moscow-1c', 'ru-moscow-1f']},
                'dms2': {'available_az': []}
            }
        }

        # Expected output
        expected_output = {
            'seaf.ta.services.dc_az': {
                'flix.dc_az.ru-moscow-1a': {
                    'title': 'ru-moscow-1a',
                    'external_id': 'ru-moscow-1a',
                    'vendor': 'Cloud.ru',
                    'region': 'flix.dc_region.russia'
                },
                'flix.dc_az.ru-moscow-1b': {
                    'title': 'ru-moscow-1b',
                    'external_id': 'ru-moscow-1b',
                    'vendor': 'Cloud.ru',
                    'region': 'flix.dc_region.russia'
                },
                'flix.dc_az.ru-moscow-1c': {
                    'title': 'ru-moscow-1c',
                    'external_id': 'ru-moscow-1c',
                    'vendor': 'Cloud.ru',
                    'region': 'flix.dc_region.russia'
                },
                'flix.dc_az.ru-moscow-1d': {
                    'title': 'ru-moscow-1d',
                    'external_id': 'ru-moscow-1d',
                    'vendor': 'Cloud.ru',
                    'region': 'flix.dc_region.russia'
                },
                'flix.dc_az.ru-moscow-1e': {
                    'title': 'ru-moscow-1e',
                    'external_id': 'ru-moscow-1e',
                    'vendor': 'Cloud.ru',
                    'region': 'flix.dc_region.russia'
                },
                'flix.dc_az.ru-moscow-1f': {
                    'title': 'ru-moscow-1f',
                    'external_id': 'ru-moscow-1f',
                    'vendor': 'Cloud.ru',
                    'region': 'flix.dc_region.russia'
                }
            }
        }

        # Run the conversion
        converted_data = convert(source_data)

        # Assert that the result is as expected
        self.assertEqual(converted_data, expected_output)

if __name__ == '__main__':
    unittest.main()
