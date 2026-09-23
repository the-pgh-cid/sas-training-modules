# Exactly three named acceptance tests; run with Rscript from any directory.
arg <- grep("^--file=", commandArgs(FALSE), value=TRUE)
if (length(arg)) {
  here <- dirname(normalizePath(sub("^--file=", "", arg[[1]])))
} else {
  paths <- lapply(sys.frames(), function(x) x$ofile)
  paths <- Filter(Negate(is.null), paths)
  if (!length(paths)) stop("Run with Rscript or source(path).")
  here <- dirname(normalizePath(tail(paths, 1)[[1]]))
}
source(file.path(here, "reference.R"))

check_expected <- function(cases, actual) {
  for (column in OUTPUTS) {
    expected <- cases[[paste0("expected_", column)]]
    value <- actual[[column]]
    if (is.numeric(expected)) {
      stopifnot(is.numeric(value), identical(is.na(value), is.na(expected)))
      keep <- !is.na(expected)
      stopifnot(isTRUE(all.equal(value[keep], expected[keep], tolerance=1e-12)))
    } else stopifnot(identical(value, expected))
  }
  for (column in INPUTS) {
    key <- paste0("expected_", column)
    if (key %in% names(cases)) stopifnot(identical(actual[[column]], cases[[key]]))
  }
}

T1_original_fixture <- function() {
  cases <- load_cases()
  cases <- cases[cases$case_id == "fixture", , drop=FALSE]
  actual <- translate(input_data(cases))
  check_expected(cases, actual)
}
T2_added_boundary <- function() {
  cases <- load_cases()
  cases <- cases[cases$case_id == "edge", , drop=FALSE]
  stopifnot(nrow(cases) > 0L)
  actual <- translate(input_data(cases))
  check_expected(cases, actual)
}
T3_preservation_type_order <- function() {
  cases <- load_cases()
  cases <- cases[rev(seq_len(nrow(cases))), , drop=FALSE]
  data <- input_data(cases)
  rownames(data) <- as.character(101L + 7L * seq_len(nrow(data)))
  before <- data
  actual <- translate(data)
  stopifnot(identical(data, before), nrow(actual) == nrow(before))
  stopifnot(identical(rownames(actual), rownames(before)))
  stopifnot(identical(names(actual), c(names(before), OUTPUTS)))
  stopifnot(identical(actual[c("case_id", "row_id")], before[c("case_id", "row_id")]))
  for (column in INPUTS) {
    if (!(column %in% names(WIDTHS))) stopifnot(identical(actual[[column]], before[[column]]))
  }
  for (column in names(WIDTHS))
    stopifnot(is.character(actual[[column]]), all(nchar(actual[[column]], type="bytes") == WIDTHS[[column]]))
  for (column in OUTPUTS) {
    if (!(column %in% names(WIDTHS))) stopifnot(is.numeric(actual[[column]]))
  }
  stopifnot(is.integer(actual$len))
  check_expected(cases, actual)
}

checks <- list(T1_original_fixture=T1_original_fixture,
               T2_added_boundary=T2_added_boundary,
               T3_preservation_type_order=T3_preservation_type_order)
for (name in names(checks)) {
  checks[[name]]()
  cat("PASS", sub("_", " ", name), "\n")
}
cat("Exactly 3 tests passed; ", R.version.string, "; base R.\n", sep="")
