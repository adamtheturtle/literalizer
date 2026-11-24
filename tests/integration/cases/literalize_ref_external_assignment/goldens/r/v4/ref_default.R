consume_widget <- function(...) NULL
ref_data <- list(
    1,
    2
)
my_data <- list(
    0
)
consume_widget(arg_value = my_data)
my_data <- ref_data
consume_widget(arg_value = my_data)
