process <- function(...) NULL
my_list <- list(
    "unused" = "value"
)
process(data = list(list(list("inner" = my_list))))
