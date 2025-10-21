import unittest
import sys
import os

# Add modules to the python path
sys.path.append(os.path.abspath('../modules'))

from dc_region_converter import convert

class TestDCRegionConverter(unittest.TestCase):

    def test_convert_dc_regions(self):
        # Sample input data with various AZs from different source entities
        source_data = {
            'seaf.ta.reverse.cloud_ru.advanced.ecss': {
                'ecs1': {'az': 'ru-moscow-1a', 'disks': [{'az': 'ru-moscow-1a'}, {'az': 'ru-moscow-1b'}]},
                'ecs2': {'az': 'ru-moscow-2c', 'disks': []}
            },
            'seaf.ta.reverse.cloud_ru.advanced.cces': {
                'cce1': {'masters_az': ['ru-moscow-1a', 'ru-moscow-2d']},
                'cce2': {'masters_az': []}
            },
            'seaf.ta.reverse.cloud_ru.advanced.rdss': {
                'rds1': {'az': ['ru-moscow-1b', 'ru-moscow-3e']},
                'rds2': {'az': []}
            },
            'seaf.ta.reverse.cloud_ru.advanced.dmss': {
                'dms1': {'available_az': ['ru-moscow-2c', 'ru-moscow-3f']},
                'dms2': {'available_az': []}
            }
        }

        # Expected output
        expected_output = {
            'seaf.ta.services.dc_region': {
                'flix.dc_region.russia': {
                    'title': 'Россия',
                    'external_id': 'russia',
                }
            }
        }

        # Run the conversion
        converted_data = convert(source_data)

        # Assert that the result is as expected
        self.assertEqual(converted_data, expected_output)

if __name__ == '__main__':
    unittest.main()
