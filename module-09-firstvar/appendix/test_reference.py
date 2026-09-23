"""Exactly three acceptance tests for one sorted nonmissing group key."""
import importlib.util
from pathlib import Path
import unittest
import pandas as pd

spec = importlib.util.spec_from_file_location('firstvar_reference', Path(__file__).with_name('reference.py'))
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)

class ReferenceTests(unittest.TestCase):
    def check_values(self, rows):
        actual = ref.translate(rows[ref.SOURCE_COLUMNS])
        for key in ['first_flag', 'last_flag']:
            self.assertEqual(actual[key].tolist(), rows['expected_' + key].tolist())

    def test_T1_original_fixture(self):
        rows = ref.load_cases()
        self.check_values(rows.loc[rows.case_id.eq('fixture')])

    def test_T2_single_row_has_both_explicit_flags(self):
        rows = ref.load_cases()
        self.check_values(rows.loc[rows.case_id.eq('edge')])

    def test_T3_preserve_rows_and_integer_flags(self):
        rows = ref.load_cases()
        source = rows.loc[rows.case_id.eq('fixture'), ref.SOURCE_COLUMNS].copy(deep=True)
        source.index = [10, 20, 30, 40, 50, 60]
        before = source.copy(deep=True)
        actual = ref.translate(source)
        self.assertIsNot(actual, source)
        pd.testing.assert_frame_equal(source, before)
        pd.testing.assert_frame_equal(actual[ref.SOURCE_COLUMNS], before)
        for key in ['first_flag', 'last_flag']:
            self.assertTrue(pd.api.types.is_integer_dtype(actual[key]))
            self.assertEqual(actual[key].tolist(), rows.loc[rows.case_id.eq('fixture'), 'expected_' + key].tolist())

if __name__ == '__main__':
    unittest.main(verbosity=2)
