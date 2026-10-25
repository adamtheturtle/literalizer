consume_widget <- function(...) NULL
shared <- list(
    1,
    2
)
my_data <- list(
    0
)
consume_widget(arg_value = my_data)
my_data <- shared
consume_widget(arg_value = my_data)
