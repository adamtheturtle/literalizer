make_widget <- function(...) NULL
consume <- function(...) NULL
my_data <- make_widget(value = 42)
consume(value = my_data)
my_data <- make_widget(value = 42)
consume(value = my_data)
