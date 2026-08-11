consume <- function(...) NULL
foo <- 42
consume(items = list(
    list(
        "other" = 1
    ),
    foo
), mapping = list(
    "left" = foo,
    "other" = 1
))
