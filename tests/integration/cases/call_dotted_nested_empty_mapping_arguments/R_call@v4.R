api.worker.process <- function(...) NULL
api.worker.process(values = list(1, list()), count = 42)
api.worker.process(values = list(2, list("x" = "s")), count = 43)
