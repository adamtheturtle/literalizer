consume_widget <- function(...) NULL
item <- list(
    1,
    2
)
my_data <- list(
    1,
    2
)
consume_widget(arg_value = my_data)
my_data <- item
consume_widget(arg_value = my_data)
