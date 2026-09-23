"""Three executable appendix tests. Shared CSV rows are the language-neutral oracle."""
from pathlib import Path
import importlib.util
import unittest
import pandas as pd
from pandas.api.types import is_numeric_dtype, is_datetime64_any_dtype

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("module07_reference", HERE / "reference.py")
reference = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reference)


class ReferenceTests(unittest.TestCase):
    def check_expected(self, output, expected):
        for col in reference.RESULT_COLUMNS:
            self.assertEqual(output[col].tolist(), expected["expected_" + col].tolist())

    def test_T1_original_fixture_known_answers(self):
        rows = reference.load_fixtures()
        rows = rows.loc[rows["case_id"].eq("fixture")]
        result = reference.translate(rows[reference.INPUT_COLUMNS])
        self.check_expected(result, rows)

    def test_T2_added_in_scope_boundaries(self):
        rows = reference.load_fixtures()
        rows = rows.loc[rows["case_id"].eq("edge")]
        result = reference.translate(rows[reference.INPUT_COLUMNS])
        self.check_expected(result, rows)

    def test_T3_preservation_types_and_order(self):
        rows = reference.load_fixtures().iloc[::-1].copy()
        rows.index = pd.Index(range(100, 100 + len(rows)), name="custom_index")
        source = rows[reference.INPUT_COLUMNS].copy(deep=True)
        before = source.copy(deep=True)
        result = reference.translate(source)
        self.assertIsNot(result, source)
        pd.testing.assert_frame_equal(source, before)
        self.assertTrue(result.index.equals(source.index))
        self.assertEqual(set(result.columns), set(reference.INPUT_COLUMNS + reference.RESULT_COLUMNS))
        self.check_expected(result, rows)
        pd.testing.assert_frame_equal(result[reference.INPUT_COLUMNS], before)
        for col in reference.RESULT_COLUMNS:
            self.assertTrue(all(isinstance(v, str) for v in result[col]), col)


if __name__ == "__main__":
    unittest.main(verbosity=2)
