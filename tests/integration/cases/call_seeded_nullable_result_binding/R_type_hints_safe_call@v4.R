make_widget <- function(...) NULL
consume <- function(...) NULL
my_data <- make_widget(count = NULL)
consume(count = my_data)
my_data <- make_widget(count = 42)
consume(count = my_data)
