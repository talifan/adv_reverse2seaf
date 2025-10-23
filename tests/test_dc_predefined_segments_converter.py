# tests/test_dc_predefined_segments_converter.py

import unittest
import os
import sys

# Add the converter modules to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))

from id_prefix import set_prefix
from dc_predefined_segments_converter import convert, PREDEFINED_SEGMENTS

set_prefix('test_prefix')

class TestDCPredefinedSegmentsConverter(unittest.TestCase):

    def test_convert_predefined_segments(self):
        """
        Tests the creation of predefined network segments for each data center.
        """
        set_prefix('test_prefix')
        source_data = {
            'seaf.ta.services.dc': {
                'test_prefix.dc.dc1': {
                    'title': 'Data Center 1',
                    'external_id': 'dc1-uuid'
                },
                'test_prefix.dc.dc2': {
                    'title': 'Data Center 2',
                    'external_id': 'dc2-uuid'
                }
            },
            '__prefix__': 'test_prefix'
        }

        converted_data = convert(source_data)
        
        # 1. Check that the main key is present
        self.assertIn('seaf.ta.services.network_segment', converted_data)
        
        segments = converted_data['seaf.ta.services.network_segment']
        
        # 2. Check the total number of segments created
        self.assertEqual(len(segments), len(PREDEFINED_SEGMENTS) * 2)
        
        # 3. Check the details of a few sample segments for each DC
        for dc_id_full, dc_details in source_data['seaf.ta.services.dc'].items():
            # Extract the simple dc_id from the full key (e.g., 'test_prefix.dc.dc1' -> 'dc1')
            dc_id = dc_id_full.split('.')[-1]
            dc_title = dc_details['title']
            
            # Check INT-NET segment
            int_net_segment_id = f"test_prefix.segment.{dc_id}.INT-NET"
            self.assertIn(int_net_segment_id, segments)
            self.assertEqual(segments[int_net_segment_id]['title'], f'INT-NET ({dc_title})')
            self.assertEqual(segments[int_net_segment_id]['location'], f'test_prefix.dc.{dc_id}')
            
            # Check INTERNET segment
            internet_segment_id = f"test_prefix.segment.{dc_id}.INTERNET"
            self.assertIn(internet_segment_id, segments)
            self.assertEqual(segments[internet_segment_id]['title'], f'INTERNET ({dc_title})')
            self.assertEqual(segments[internet_segment_id]['location'], f'test_prefix.dc.{dc_id}')
            self.assertEqual(segments[internet_segment_id]['zone'], 'INTERNET')

if __name__ == '__main__':
    unittest.main()
