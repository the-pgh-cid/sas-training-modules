# One sorted, nonmissing group key; explicit endpoints preserve singleton groups.
source_columns <- c('id', 'group', 'value')
translate <- function(df) {
  out <- df
  g <- out$group
  n <- length(g)
  if (anyNA(g) || is.unsorted(g)) stop('Expected sorted, nonmissing groups')
  first <- last <- integer(n)
  if (n > 0L) {
    first[1L] <- 1L
    last[n] <- 1L
    if (n > 1L) {
      change <- g[-1L] != g[-n]
      first[-1L] <- as.integer(change)
      last[-n] <- as.integer(change)
    }
  }
  out$first_flag <- first
  out$last_flag <- last
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
  for (key in c('id', 'value', 'expected_first_flag', 'expected_last_flag'))
    x[[key]] <- as.integer(x[[key]])
  x
}
if (sys.nframe() == 0L) {
  x <- load_cases()
  print(translate(x[x$case_id == 'fixture', source_columns, drop = FALSE]))
}
