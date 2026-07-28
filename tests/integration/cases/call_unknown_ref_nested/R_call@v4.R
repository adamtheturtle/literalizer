process <- function(...) NULL
known_value <- TRUE
unknown_value <- TRUE
process(known_value = known_value, nested_missing = list(unknown_value))
