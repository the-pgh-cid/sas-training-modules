# Exactly three named tests; run with Rscript /absolute/path/test_reference.R.
file_arg <- grep('^--file=', commandArgs(FALSE), value = TRUE)
if (!length(file_arg)) stop('Use Rscript or the documented WebR runner')
here <- dirname(normalizePath(sub('^--file=', '', file_arg[[1]])))
source(file.path(here, 'reference.R'))
cases <- load_cases()
assert_equal <- function(actual, expected) {
  stopifnot(isTRUE(all.equal(actual, expected, check.attributes = FALSE)))
}
results <- c('prev_value', 'prev2_value', 'change')
check_values <- function(rows) {
  actual <- translate(rows[, source_columns, drop = FALSE])
  for (key in results) {
    gold <- rows[[paste0('expected_', key)]]
    stopifnot(identical(is.na(actual[[key]]), is.na(gold)))
    assert_equal(actual[[key]], gold)
  }
}
test_T1_original_fixture <- function() {
  check_values(cases[cases$case_id == 'fixture', , drop = FALSE])
}
test_T2_single_row_has_no_history <- function() {
  check_values(cases[cases$case_id == 'edge', , drop = FALSE])
}
test_T3_preserve_order_missing_and_numeric_types <- function() {
  rows <- cases[cases$case_id == 'fixture', , drop = FALSE]
  input <- rows[, source_columns, drop = FALSE]
  rownames(input) <- as.character(seq_len(nrow(input)) * 10L)
  before <- input
  actual <- translate(input)
  stopifnot(identical(input, before), identical(actual[source_columns], before))
  for (key in results) {
    stopifnot(is.numeric(actual[[key]]))
    assert_equal(actual[[key]], rows[[paste0('expected_', key)]])
    stopifnot(identical(is.na(actual[[key]]), is.na(rows[[paste0('expected_', key)]])))
  }
}

test_T1_original_fixture(); cat("PASS T1 original_fixture\n")
test_T2_single_row_has_no_history(); cat("PASS T2 single_row_has_no_history\n")
test_T3_preserve_order_missing_and_numeric_types(); cat("PASS T3 preserve_order_missing_and_numeric_types\n")
