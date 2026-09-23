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
  assert_equal(actual$num_value, rows$expected_num_value)
  assert_equal(actual$date_value, rows$expected_date_value)
}
test_T1_original_fixture <- function() {
  check_values(cases[cases$case_id == 'fixture', , drop = FALSE])
}
test_T2_valid_leap_day_and_numeric_boundary <- function() {
  check_values(cases[cases$case_id == 'edge', , drop = FALSE])
}
test_T3_source_order_and_result_types <- function() {
  input <- cases[rev(seq_len(nrow(cases))), source_columns, drop = FALSE]
  before <- input
  actual <- translate(input)
  stopifnot(identical(input, before), identical(actual[source_columns], before))
  stopifnot(is.numeric(actual$num_value), inherits(actual$date_value, 'Date'))
  stopifnot(is.character(actual$char_num), is.character(actual$char_date))
  stopifnot('0012' %in% actual$char_num)
}

test_T1_original_fixture(); cat("PASS T1 original_fixture\n")
test_T2_valid_leap_day_and_numeric_boundary(); cat("PASS T2 valid_leap_day_and_numeric_boundary\n")
test_T3_source_order_and_result_types(); cat("PASS T3 source_order_and_result_types\n")
