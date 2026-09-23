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
INPUTS <- c("first", "middle", "last")
OUTPUTS <- c("name1", "name2")
NUMERIC <- character()
WIDTHS <- c(first=8L,middle=8L,last=8L,name1=24L,name2=24L)

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

catx_space <- function(v) {
  v <- trimws(v, whitespace=" ")
  paste(v[nzchar(v)], collapse=" ")
}

translate <- function(df) {
  out <- df
  cols <- c("first", "middle", "last")
  for (col in cols)
    out[[col]] <- sprintf(
      "%-8s", out[[col]])
  out$name1 <- paste0(
    out$first, out$middle, out$last)
  a <- apply(out[cols], 1, catx_space)
  out$name2 <- sprintf("%-24s", a)
  out
}

if (sys.nframe() == 0L) {
  cases <- load_cases()
  print(translate(input_data(cases[cases$case_id == "fixture", , drop=FALSE])))
}
