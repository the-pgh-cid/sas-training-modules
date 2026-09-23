# Appendix reference; not a historical response or general SAS emulator.
script_dir <- function() {
  arg <- grep("^--file=", commandArgs(FALSE), value=TRUE)
  if (!length(arg)) stop("Run with Rscript and an absolute or relative script path")
  dirname(normalizePath(sub("^--file=", "", arg[[1]])))
}
HERE <- script_dir()
INPUT_COLUMNS <- c("case_id", "row_id", "text")
RESULT_COLUMNS <- c("no_spaces", "no_digits", "only_letters")

load_fixtures <- function(path=file.path(HERE, "fixtures.csv")) {
  df <- read.csv(path, colClasses="character", check.names=FALSE,
                 stringsAsFactors=FALSE, na.strings="__MISSING__",
                 strip.white=FALSE)
  df$row_id <- as.integer(df$row_id)
  df
}

translate <- function(df) {
  out <- df
  out$no_spaces <- gsub(
    " ", "", out$text, fixed=TRUE)
  out$no_digits <- gsub(
    "[0-9]", "", out$text)
  out$only_letters <- gsub(
    "[^A-Za-z]", "", out$text)
  out
}

if (sys.nframe() == 0L) {
  fixture <- load_fixtures()
  fixture <- fixture[fixture$case_id == "fixture", INPUT_COLUMNS, drop=FALSE]
  print(translate(fixture), row.names=FALSE)
}
