make_widget <- function(...) NULL
make_widget(before = list(), populated = list(1), after = list())
make_widget(before = list("text"), populated = list(2), after = list())
make_widget(before = list(), populated = list("text"), after = list())
make_widget(before = list("text"), populated = list(2), after = list(3))
