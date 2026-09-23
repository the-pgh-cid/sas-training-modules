# Executable base R reference; not a replay of an LLM response.
script_path <- function() {
  frames <- sys.frames()
  for (i in rev(seq_along(frames))) {
    if (!is.null(frames[[i]]$ofile))
      return(normalizePath(frames[[i]]$ofile))
  }
  arg <- grep("^--file=", commandArgs(FALSE), value=TRUE)
  if (length(arg)) return(normalizePath(sub("^--file=", "", arg[[1]])))
  stop("Run with Rscript or source() using a file path.")
}
reference_dir <- dirname(script_path())
INPUTS <- c("x", "y", "z")
OUTPUTS <- c("average")
NUMERIC <- c("x", "y", "z", "expected_average")
WIDTHS <- integer()

load_cases <- function() {
  data <- read.csv(file.path(reference_dir, "fixtures.csv"),
    colClasses="character", strip.white=FALSE, na.strings=character(),
    check.names=FALSE, stringsAsFactors=FALSE)
  for (column in NUMERIC) {
    v <- data[[column]]
    v[v == "__MISSING__"] <- NA_character_
    data[[column]] <- as.numeric(v)
  }
  data
}
input_data <- function(cases) {
  cases[c("case_id", "row_id", INPUTS)]
}

translate <- function(df) {
  out <- df
  cols <- c("x", "y", "z")
  a <- rowMeans(out[cols], na.rm=TRUE)
  a[is.nan(a)] <- NA_real_
  out$average <- a
  out
}

if (sys.nframe() == 0L) {
  cases <- load_cases()
  print(translate(input_data(cases[cases$case_id == "fixture", , drop=FALSE])))
}
