process <- function(...) NULL
emit <- function(...) NULL
emit(process(value = "hello"), "one")
emit(process(value = 42), "zero")
