# Appendix reference; not a historical response or general SAS emulator.
script_dir <- function() {
  arg <- grep("^--file=", commandArgs(FALSE), value=TRUE)
  if (!length(arg)) stop("Run with Rscript and an absolute or relative script path")
  dirname(normalizePath(sub("^--file=", "", arg[[1]])))
}
HERE <- script_dir()
INPUT_COLUMNS <- c("case_id", "row_id", "start_date", "end_date")
RESULT_COLUMNS <- c("days", "months", "years")

load_fixtures <- function(path=file.path(HERE, "fixtures.csv")) {
  df <- read.csv(path, colClasses="character", check.names=FALSE,
                 stringsAsFactors=FALSE, na.strings="__MISSING__",
                 strip.white=FALSE)
  df$row_id <- as.integer(df$row_id)
  df$expected_days <- as.numeric(df$expected_days)
  df$expected_months <- as.numeric(df$expected_months)
  df$expected_years <- as.numeric(df$expected_years)
  df
}

# month.abb is the built-in English month-name vector.
parse_date9 <- function(x) {
  month <- match(substr(x, 3, 5), toupper(month.abb))
  iso <- sprintf("%s-%02d-%s", substr(x, 6, 9), month, substr(x, 1, 2))
  as.Date(iso, format="%Y-%m-%d")
}
part <- function(x, pattern) as.integer(format(x, pattern))

translate <- function(df) {
  out <- df
  out$start_date <- parse_date9(
    out$start_date)
  out$end_date <- parse_date9(out$end_date)
  s <- out$start_date
  e <- out$end_date
  out$days <- as.integer(e - s)
  out$years <- part(e,"%Y") - part(s,"%Y")
  out$months <- 12*out$years +
    part(e,"%m") - part(s,"%m")
  out
}

if (sys.nframe() == 0L) {
  fixture <- load_fixtures()
  fixture <- fixture[fixture$case_id == "fixture", INPUT_COLUMNS, drop=FALSE]
  print(translate(fixture), row.names=FALSE)
}
