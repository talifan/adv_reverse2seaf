import unittest
import sys
import os

# Debug prints
print(f"__file__: {__file__}")
print(f"os.path.dirname(__file__): {os.path.dirname(__file__)}")
print(f"os.path.join(os.path.dirname(__file__), '..', 'modules'): {os.path.join(os.path.dirname(__file__), '..', 'modules')}")
print(f"os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules')): {os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules'))}")
print(f"os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')): {os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils'))}")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))
sys.path.append(os.path.abspath('_metamodel_/iaas/converter/utils'))

print(f"sys.path after append: {sys.path}")

from id_prefix import set_prefix
from dc_converter import convert
from warning_reporter import get_collected_warnings, clear_collected_warnings # Import for testing warnings

set_prefix('tenant')

class TestDcConverter(unittest.TestCase):

    def setUp(self):
        clear_collected_warnings() # Clear warnings before each test

    def test_convert_dcs_from_azs(self):
        source_data = {
            'seaf.ta.reverse.cloud_ru.advanced.ecss': {
                'ecs1': {
                    'az': 'ru-moscow-1a',
                    'disks': [{'disk-uuid-1': {'az': 'ru-moscow-1b'}}]
                },
                'ecs2': {
                    'az': 'c' # Invalid single character
                },
                'ecs3': {
                    'az': None # Missing AZ
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
                'tenant.dc.ru-moscow-1a': {
                    'title': 'ru-moscow-1a',
                    'external_id': 'ru-moscow-1a',
                    'type': 'Облачный',
                    'vendor': 'Cloud.ru',
                    'address': 'ru-moscow-1a',
                    'availabilityzone': 'tenant.dc_az.ru-moscow-1a'
                },
                'tenant.dc.ru-moscow-1b': {
                    'title': 'ru-moscow-1b',
                    'external_id': 'ru-moscow-1b',
                    'type': 'Облачный',
                    'vendor': 'Cloud.ru',
                    'address': 'ru-moscow-1b',
                    'availabilityzone': 'tenant.dc_az.ru-moscow-1b'
                },
                'tenant.dc.ru-moscow-1c': {
                    'title': 'ru-moscow-1c',
                    'external_id': 'ru-moscow-1c',
                    'type': 'Облачный',
                    'vendor': 'Cloud.ru',
                    'address': 'ru-moscow-1c',
                    'availabilityzone': 'tenant.dc_az.ru-moscow-1c'
                },
                'tenant.dc.ru-moscow-1d': {
                    'title': 'ru-moscow-1d',
                    'external_id': 'ru-moscow-1d',
                    'type': 'Облачный',
                    'vendor': 'Cloud.ru',
                    'address': 'ru-moscow-1d',
                    'availabilityzone': 'tenant.dc_az.ru-moscow-1d'
                },
                'tenant.dc.ru-moscow-1e': {
                    'title': 'ru-moscow-1e',
                    'external_id': 'ru-moscow-1e',
                    'type': 'Облачный',
                    'vendor': 'Cloud.ru',
                    'address': 'ru-moscow-1e',
                    'availabilityzone': 'tenant.dc_az.ru-moscow-1e'
                }
            }
        }
        converted_data = convert(source_data)
        self.assertEqual(converted_data, expected_output)

        # Assert warnings
        warnings = get_collected_warnings()
        self.assertIn("WARNING: Entity 'ecs2' - Field 'az': Invalid AZ name 'c' (too short). Skipping.", warnings)
        self.assertIn("WARNING: Entity 'cce1' - Field 'masters_az': Invalid AZ name 'inv' (too short) in list. Skipping.", warnings)
        self.assertIn("WARNING: Entity 'dms1' - Field 'available_az': Invalid AZ entry 'None' (not a string) in list. Skipping.", warnings)
        self.assertIn("WARNING: Entity 'dms1' - Field 'available_az': Invalid AZ entry '123' (not a string) in list. Skipping.", warnings)
        self.assertEqual(len(warnings), 4)

if __name__ == '__main__':
    unittest.main()
