process <- function(...) NULL
emit <- function(...) NULL
emit(process(value = "hello"), list("a" = 1, "b" = 2))
emit(process(value = 42), list("c" = 3, "d" = 4))
