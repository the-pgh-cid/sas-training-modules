# Each original SAS LAG occurrence executes once on every row; no stats::lag.
source_columns <- c('id', 'value')
lag_rows <- function(x, k) {
  n <- length(x)
  if (n == 0L) return(numeric(0))
  k <- min(as.integer(k), n)
  c(rep(NA_real_, k), head(x, n - k))
}
translate <- function(df) {
  out <- df
  out$prev_value <- lag_rows(out$value, 1L)
  out$prev2_value <- lag_rows(out$value, 2L)
  out$change <- out$value - out$prev_value
  out
}
appendix_dir <- function() {
  arg <- grep('^--file=', commandArgs(FALSE), value = TRUE)
  if (length(arg)) return(dirname(normalizePath(sub('^--file=', '', arg[[1]]))))
  stop('Run with Rscript /absolute/path/reference.R or test_reference.R')
}
load_cases <- function() {
  x <- read.csv(file.path(appendix_dir(), 'fixtures.csv'),
                colClasses = 'character', strip.white = FALSE,
                na.strings = '__MISSING__', check.names = FALSE)
  for (key in c('id', 'value', 'expected_prev_value', 'expected_prev2_value', 'expected_change'))
    x[[key]] <- as.numeric(x[[key]])
  x
}
if (sys.nframe() == 0L) {
  x <- load_cases()
  print(translate(x[x$case_id == 'fixture', source_columns, drop = FALSE]))
}
