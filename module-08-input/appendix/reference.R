# Valid English inputs; returns numeric and Date columns, retaining source text.
source_columns <- c('char_num', 'char_date')
translate <- function(df) {
  out <- df
  out$num_value <- as.numeric(out$char_num)
  old_locale <- Sys.getlocale('LC_TIME')
  on.exit(Sys.setlocale(
    'LC_TIME', old_locale))
  changed <- Sys.setlocale('LC_TIME', 'C')
  if (changed == '') stop('C unavailable')
  out$date_value <- as.Date(
    out$char_date, format = '%d%b%Y')
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
  x$row_id <- as.integer(x$row_id)
  x$expected_num_value <- as.numeric(x$expected_num_value)
  x$expected_date_value <- as.Date(x$expected_date_value)
  x
}
if (sys.nframe() == 0L) {
  x <- load_cases()
  print(translate(x[x$case_id == 'fixture', source_columns, drop = FALSE]))
}
