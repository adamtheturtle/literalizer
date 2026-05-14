process <- function(...) NULL
my_ints <- list(
    1,
    2,
    3
)
my_strings <- list(
    "a",
    "b"
)
my_empty <- list()
process(data = my_ints, count = 42)
process(data = my_strings, count = 7)
process(data = my_empty, count = 99)
