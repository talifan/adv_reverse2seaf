import unittest
import sys
import os

# Add modules to the python path
sys.path.append(os.path.abspath('_metamodel_/iaas/converter/modules'))
sys.path.append(os.path.abspath('_metamodel_/iaas/converter/utils'))

from id_prefix import set_prefix
from branches_converter import convert

set_prefix('tenant')

class TestBranchesConverter(unittest.TestCase):

    def test_convert_branches(self):
        # Sample input data for branches
        source_data = {
            'seaf.ta.reverse.cloud_ru.advanced.branches': {
                'tenant.branches.kremlin': {
                    'id': 'kremlin',
                    'name': 'Кремль',
                    'country': 'Россия',
                    'city': 'Москва',
                    'location': 'Красная площадь 1',
                    'symbol': 'svg_branch'
                },
                'tenant.branches.spb': {
                    'id': 'spb',
                    'name': 'Смольный',
                    'country': 'Россия',
                    'city': 'Санкт-Петербург',
                    'location': 'Смольный проезд 1',
                    'symbol': 'svg_branch'
                }
            }
        }

        # Expected output
        expected_output = {
            'seaf.ta.services.office': {
                'tenant.branches.kremlin': {
                    'title': 'Кремль',
                    'description': 'Symbol: svg_branch',
                    'external_id': 'kremlin',
                    'address': 'Красная площадь 1',
                    'region': 'tenant.dc_region.россия_москва'
                },
                'tenant.branches.spb': {
                    'title': 'Смольный',
                    'description': 'Symbol: svg_branch',
                    'external_id': 'spb',
                    'address': 'Смольный проезд 1',
                    'region': 'tenant.dc_region.россия_санкт-петербург'
                }
            }
        }

        # Run the conversion
        converted_data = convert(source_data)

        # Assert that the result is as expected
        self.assertEqual(converted_data, expected_output)

if __name__ == '__main__':
    unittest.main()
