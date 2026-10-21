thing.go <- function(...) NULL
thing.go(before = list(), populated = list(1), after = list())
thing.go(before = list("text"), populated = list(2), after = list())
thing.go(before = list(), populated = list("text"), after = list())
thing.go(before = list("text"), populated = list(2), after = list(3))
