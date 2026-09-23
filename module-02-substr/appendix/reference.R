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
INPUTS <- c("text")
OUTPUTS <- c("first_three", "middle", "from_seventh")
NUMERIC <- character()
WIDTHS <- c(text=20L,first_three=3L,middle=4L,from_seventh=14L)

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
  out$text <- sprintf("%-20s", out$text)
  s <- out$text
  out$first_three <- substr(s, 1, 3)
  out$middle <- substr(s, 5, 8)
  out$from_seventh <- substr(s, 7, 20)
  out
}

if (sys.nframe() == 0L) {
  cases <- load_cases()
  print(translate(input_data(cases[cases$case_id == "fixture", , drop=FALSE])))
}
