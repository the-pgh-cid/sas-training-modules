# Exactly three named tests, using base R assertions and the shared CSV oracle.
file_arg <- grep("^--file=", commandArgs(FALSE), value=TRUE)
if (!length(file_arg)) stop("Run this file with Rscript")
here <- dirname(normalizePath(sub("^--file=", "", file_arg[[1]])))
ref <- new.env(parent=globalenv())
source(file.path(here, "reference.R"), local=ref)

check_expected <- function(out, expected) {
  for (col in ref$RESULT_COLUMNS) {
    actual <- out[[col]]
    wanted <- expected[[paste0("expected_", col)]]
    if (is.numeric(wanted)) {
      stopifnot(identical(as.numeric(actual), as.numeric(wanted)))
    } else {
      stopifnot(identical(as.character(actual), as.character(wanted)))
    }
  }
}

test_T1_original_fixture_known_answers <- function() {
  rows <- ref$load_fixtures()
  rows <- rows[rows$case_id == "fixture", , drop=FALSE]
  out <- ref$translate(rows[, ref$INPUT_COLUMNS, drop=FALSE])
  check_expected(out, rows)
}

test_T2_added_in_scope_boundaries <- function() {
  rows <- ref$load_fixtures()
  rows <- rows[rows$case_id == "edge", , drop=FALSE]
  out <- ref$translate(rows[, ref$INPUT_COLUMNS, drop=FALSE])
  check_expected(out, rows)
}

test_T3_preservation_types_and_order <- function() {
  rows <- ref$load_fixtures()
  rows <- rows[rev(seq_len(nrow(rows))), , drop=FALSE]
  rownames(rows) <- paste0("custom_", seq_len(nrow(rows)))
  source <- rows[, ref$INPUT_COLUMNS, drop=FALSE]
  before <- source
  out <- ref$translate(source)
  stopifnot(identical(source, before), identical(rownames(out), rownames(source)),
            setequal(names(out), c(ref$INPUT_COLUMNS, ref$RESULT_COLUMNS)))
  check_expected(out, rows)
  stopifnot(identical(out[, ref$INPUT_COLUMNS, drop=FALSE], before))
  stopifnot(all(vapply(out[ref$RESULT_COLUMNS], is.character, logical(1))))
}

cases <- list(T1=test_T1_original_fixture_known_answers,
              T2=test_T2_added_in_scope_boundaries,
              T3=test_T3_preservation_types_and_order)
for (name in names(cases)) {
  cases[[name]]()
  cat("PASS", name, "\n")
}
cat("3 named tests passed;", R.version.string, "\n")
