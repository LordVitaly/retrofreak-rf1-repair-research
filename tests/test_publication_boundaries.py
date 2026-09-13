"""Regression tests for device maps that escaped the original publication scan."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from check_repository import private_device_arrays


class DeviceMapTests(unittest.TestCase):
    def test_nested_complete_maps_are_rejected(self):
        record = {'result': {'before_mapping': list(range(1896)),
                             'reopened_mapping': list(range(1896))}}
        self.assertEqual(private_device_arrays(record),
                         ['/result/before_mapping', '/result/reopened_mapping'])

    def test_list_nested_mapping_is_rejected(self):
        self.assertEqual(private_device_arrays({'runs': [{'logical_to_physical': list(range(128))}]}),
                         ['/runs/0/logical_to_physical'])

    def test_device_lists_are_rejected(self):
        self.assertEqual(private_device_arrays({'baseline_protected_blocks': [0, 1, 2]}),
                         ['/baseline_protected_blocks'])
        self.assertEqual(private_device_arrays({'bad_block_list': [44]}), ['/bad_block_list'])

    def test_evidence_summary_and_native_statuses_are_retained(self):
        record = {'mapping_entries': 1896, 'native_page_rc': [0]*256,
                  'input_map_first24': list(range(24)),
                  'selected_boot_mapping': [74, 23, 24, 77, 78],
                  'changes': [{'logical_block': 24, 'before_physical': 52, 'after_physical': 1056}]}
        self.assertEqual(private_device_arrays(record), [])

    def test_command_logs_and_redacted_text_are_not_numeric_maps(self):
        self.assertEqual(private_device_arrays({'commands': ['synthetic command']*1896,
                                                'before_mapping': ['REDACTED']*1896}), [])


if __name__ == '__main__':
    unittest.main()
