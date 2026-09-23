"""Exactly three acceptance tests against the executable reference."""
import importlib.util
from pathlib import Path
import unittest
import pandas as pd

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("appendix_reference", HERE / "reference.py")
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)


def check_expected(test, cases, actual):
    for column in ref.OUTPUTS:
        pd.testing.assert_series_equal(actual[column].reset_index(drop=True),
            cases["expected_" + column].reset_index(drop=True),
            check_names=False, check_dtype=False)
    for column in ref.INPUTS:
        key = "expected_" + column
        if key in cases:
            test.assertEqual(actual[column].tolist(), cases[key].tolist())


class ReferenceTests(unittest.TestCase):
    def test_T1_original_fixture(self):
        cases = ref.load_cases().query("case_id == 'fixture'")
        actual = ref.translate(ref.input_data(cases))
        check_expected(self, cases, actual)

    def test_T2_added_boundary(self):
        cases = ref.load_cases().query("case_id == 'edge'")
        self.assertGreater(len(cases), 0)
        actual = ref.translate(ref.input_data(cases))
        check_expected(self, cases, actual)

    def test_T3_preservation_type_order(self):
        cases = ref.load_cases().iloc[::-1].copy(deep=True)
        data = ref.input_data(cases)
        data.index = [101 + 7 * i for i in range(len(data))]
        before = data.copy(deep=True)
        actual = ref.translate(data)
        self.assertIsNot(actual, data)
        pd.testing.assert_frame_equal(data, before)
        self.assertEqual(len(actual), len(before))
        self.assertTrue(actual.index.equals(before.index))
        self.assertEqual(actual.columns.tolist(), before.columns.tolist() + ref.OUTPUTS)
        pd.testing.assert_frame_equal(actual[["case_id", "row_id"]], before[["case_id", "row_id"]])
        for column in ref.INPUTS:
            if column not in ref.WIDTHS:
                pd.testing.assert_series_equal(actual[column], before[column])
        for column, width in ref.WIDTHS.items():
            self.assertTrue(actual[column].map(lambda v: isinstance(v, str)).all())
            self.assertTrue(actual[column].str.len().eq(width).all())
        for column in ref.OUTPUTS:
            if column not in ref.WIDTHS:
                self.assertTrue(pd.api.types.is_numeric_dtype(actual[column]))
        pass
        check_expected(self, cases, actual)


if __name__ == "__main__":
    unittest.main(verbosity=2)
