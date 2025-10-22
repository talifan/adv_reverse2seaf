import unittest
import sys
import os

sys.path.append(os.path.abspath('_metamodel_/iaas/converter/modules'))

from dc_converter import convert

class TestDcConverter(unittest.TestCase):
    def test_convert_dcs_from_azs(self):
        source_data = {
            'seaf.ta.reverse.cloud_ru.advanced.ecss': {
                'ecs1': {
                    'az': 'ru-moscow-1a',
                    'disks': [{'disk-uuid-1': {'az': 'ru-moscow-1b'}}]
                },
                'ecs2': {
                    'az': 'c' # Invalid single character
                }
            },
            'seaf.ta.reverse.cloud_ru.advanced.cces': {
                'cce1': {'masters_az': ['ru-moscow-1a', 'ru-moscow-1c', 'inv']} # 'inv' is invalid
            },
            'seaf.ta.reverse.cloud_ru.advanced.rdss': {
                'rds1': {'az': 'ru-moscow-1d'} # This is a string, not a list
            },
            'seaf.ta.reverse.cloud_ru.advanced.dmss': {
                'dms1': {'available_az': ['ru-moscow-1d', 'ru-moscow-1e', None, 123] } # Contains invalid types
            }
        }
        expected_output = {
            'seaf.ta.services.dc': {
                'flix.dc.ru-moscow-1a': {
                    'title': 'ru-moscow-1a',
                    'external_id': 'ru-moscow-1a',
                    'type': 'Облачный',
                    'vendor': 'Cloud.ru',
                    'address': 'ru-moscow-1a',
                    'availabilityzone': 'flix.dc_az.ru-moscow-1a'
                },
                'flix.dc.ru-moscow-1b': {
                    'title': 'ru-moscow-1b',
                    'external_id': 'ru-moscow-1b',
                    'type': 'Облачный',
                    'vendor': 'Cloud.ru',
                    'address': 'ru-moscow-1b',
                    'availabilityzone': 'flix.dc_az.ru-moscow-1b'
                },
                'flix.dc.ru-moscow-1c': {
                    'title': 'ru-moscow-1c',
                    'external_id': 'ru-moscow-1c',
                    'type': 'Облачный',
                    'vendor': 'Cloud.ru',
                    'address': 'ru-moscow-1c',
                    'availabilityzone': 'flix.dc_az.ru-moscow-1c'
                },
                'flix.dc.ru-moscow-1d': {
                    'title': 'ru-moscow-1d',
                    'external_id': 'ru-moscow-1d',
                    'type': 'Облачный',
                    'vendor': 'Cloud.ru',
                    'address': 'ru-moscow-1d',
                    'availabilityzone': 'flix.dc_az.ru-moscow-1d'
                },
                'flix.dc.ru-moscow-1e': {
                    'title': 'ru-moscow-1e',
                    'external_id': 'ru-moscow-1e',
                    'type': 'Облачный',
                    'vendor': 'Cloud.ru',
                    'address': 'ru-moscow-1e',
                    'availabilityzone': 'flix.dc_az.ru-moscow-1e'
                }
            }
        }
        converted_data = convert(source_data)
        self.assertEqual(converted_data, expected_output)

if __name__ == '__main__':
    unittest.main()
