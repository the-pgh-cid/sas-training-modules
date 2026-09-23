# Exactly three named tests; run with Rscript /absolute/path/test_reference.R.
file_arg <- grep('^--file=', commandArgs(FALSE), value = TRUE)
if (!length(file_arg)) stop('Use Rscript or the documented WebR runner')
here <- dirname(normalizePath(sub('^--file=', '', file_arg[[1]])))
source(file.path(here, 'reference.R'))
cases <- load_cases()
assert_equal <- function(actual, expected) {
  stopifnot(isTRUE(all.equal(actual, expected, check.attributes = FALSE)))
}
check_values <- function(rows) {
  actual <- translate(rows[, source_columns, drop = FALSE])
  assert_equal(actual$first_flag, rows$expected_first_flag)
  assert_equal(actual$last_flag, rows$expected_last_flag)
}
test_T1_original_fixture <- function() {
  check_values(cases[cases$case_id == 'fixture', , drop = FALSE])
}
test_T2_single_row_has_both_explicit_flags <- function() {
  check_values(cases[cases$case_id == 'edge', , drop = FALSE])
}
test_T3_preserve_rows_and_integer_flags <- function() {
  rows <- cases[cases$case_id == 'fixture', , drop = FALSE]
  input <- rows[, source_columns, drop = FALSE]
  rownames(input) <- as.character(seq_len(nrow(input)) * 10L)
  before <- input
  actual <- translate(input)
  stopifnot(identical(input, before), identical(actual[source_columns], before))
  stopifnot(is.integer(actual$first_flag), is.integer(actual$last_flag))
  assert_equal(actual$first_flag, rows$expected_first_flag)
  assert_equal(actual$last_flag, rows$expected_last_flag)
}

test_T1_original_fixture(); cat("PASS T1 original_fixture\n")
test_T2_single_row_has_both_explicit_flags(); cat("PASS T2 single_row_has_both_explicit_flags\n")
test_T3_preserve_rows_and_integer_flags(); cat("PASS T3 preserve_rows_and_integer_flags\n")
