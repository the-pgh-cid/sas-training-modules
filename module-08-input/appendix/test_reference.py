"""Exactly three acceptance tests; added valid cases do not change trial scores."""
import importlib.util
from pathlib import Path
import unittest
import pandas as pd

spec = importlib.util.spec_from_file_location('input_reference', Path(__file__).with_name('reference.py'))
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)

class ReferenceTests(unittest.TestCase):
    def check_values(self, rows):
        actual = ref.translate(rows[ref.SOURCE_COLUMNS])
        self.assertEqual(actual['num_value'].tolist(), rows['expected_num_value'].tolist())
        self.assertEqual(actual['date_value'].dt.strftime('%Y-%m-%d').tolist(), rows['expected_date_value'].tolist())

    def test_T1_original_fixture(self):
        rows = ref.load_cases()
        self.check_values(rows.loc[rows.case_id.eq('fixture')])

    def test_T2_valid_leap_day_and_numeric_boundary(self):
        rows = ref.load_cases()
        self.check_values(rows.loc[rows.case_id.eq('edge')])

    def test_T3_source_order_and_result_types(self):
        source = ref.load_cases()[ref.SOURCE_COLUMNS].iloc[::-1].copy(deep=True)
        before = source.copy(deep=True)
        actual = ref.translate(source)
        self.assertIsNot(actual, source)
        pd.testing.assert_frame_equal(source, before)
        pd.testing.assert_frame_equal(actual[ref.SOURCE_COLUMNS], before)
        self.assertTrue(pd.api.types.is_numeric_dtype(actual['num_value']))
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(actual['date_value']))
        self.assertTrue(all(isinstance(v, str) for v in actual['char_num']))
        self.assertTrue(all(isinstance(v, str) for v in actual['char_date']))
        self.assertIn('0012', actual['char_num'].tolist())

if __name__ == '__main__':
    unittest.main(verbosity=2)
