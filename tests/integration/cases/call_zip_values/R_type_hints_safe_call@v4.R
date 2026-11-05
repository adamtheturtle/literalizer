process <- function(...) NULL
emit <- function(...) NULL
emit(process(value = "hello"), TRUE)
emit(process(value = 42), FALSE)
