"""Three named acceptance tests for the MEAN pilot, adapted from module 01.
Expected values must be supplied separately from the candidate calculation.
The callable runs ordinary Python. This harness is not a security sandbox.
"""
import io
import unittest
from typing import Callable, TextIO
import pandas as pd

INPUT_COLUMNS = ["case_id", "row_id", "x", "y", "z"]
MEASUREMENT_COLUMNS = ["x", "y", "z"]


def load_cases(csv_text: str) -> pd.DataFrame:
    """Decode the explicit missing sentinel; do not infer label missingness."""
    cases = pd.read_csv(io.StringIO(csv_text), dtype=str,
                        keep_default_na=False, na_filter=False)
    for col in MEASUREMENT_COLUMNS + ["expected_average"]:
        cases[col] = pd.to_numeric(cases[col].replace(
            "__MISSING__", float("nan")), errors="raise").astype("float64")
    if cases["row_id"].duplicated().any():
        raise ValueError("Fixture row_id values must be unique.")
    return cases


def run_acceptance(transform: Callable[[pd.DataFrame], pd.DataFrame],
                   cases: pd.DataFrame, stream: TextIO | None = None
                   ) -> unittest.TestResult:
    """Run T1, T2 and T3 against the supplied callable; return real results."""
    if not callable(transform):
        raise TypeError("transform must be a reviewed callable.")

    def check_values(actual: pd.DataFrame, expected_cases: pd.DataFrame) -> None:
        if not isinstance(actual, pd.DataFrame):
            raise AssertionError("The candidate must return a pandas DataFrame.")
        pd.testing.assert_series_equal(
            actual["average"].reset_index(drop=True),
            expected_cases["expected_average"].reset_index(drop=True),
            check_names=False, check_dtype=False, check_exact=True)

    class AcceptanceTests(unittest.TestCase):
        def test_T1_known_answers(self):
            subset = cases.loc[cases["case_id"].eq("fixture")].copy(deep=True)
            self.assertEqual(len(subset), 3)
            actual = transform(subset[INPUT_COLUMNS].copy(deep=True))
            check_values(actual, subset)

        def test_T2_discriminating_cases(self):
            subset = cases.loc[cases["case_id"].eq("edge")].copy(deep=True)
            self.assertEqual(len(subset), 2)
            actual = transform(subset[INPUT_COLUMNS].copy(deep=True))
            check_values(actual, subset)

        def test_T3_preservation(self):
            # Reversal and non-default index expose accidental reordering/reset.
            subset = cases.iloc[::-1].copy(deep=True)
            data = subset[INPUT_COLUMNS].copy(deep=True)
            data.index = [101 + 7 * i for i in range(len(data))]
            before = data.copy(deep=True)
            actual = transform(data)
            self.assertIsInstance(actual, pd.DataFrame)
            self.assertIsNot(actual, data)
            pd.testing.assert_frame_equal(data, before, check_exact=True)
            self.assertEqual(len(actual), len(before))
            self.assertTrue(actual.index.equals(before.index))
            self.assertEqual(actual.columns.tolist(),
                             before.columns.tolist() + ["average"])
            pd.testing.assert_frame_equal(actual[INPUT_COLUMNS], before,
                                          check_exact=True)
            self.assertTrue(pd.api.types.is_numeric_dtype(actual["average"]))
            self.assertFalse(pd.api.types.is_bool_dtype(actual["average"]))
            check_values(actual, subset)

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(AcceptanceTests)
    return unittest.TextTestRunner(verbosity=2, stream=stream).run(suite)
