process <- function(...) NULL
my_var <- 42
my_other <- 7
process(data = list(list("ref" = "my_var"), 42, "static"))
process(data = list(list("ref" = "my_other"), 7, "label"))
