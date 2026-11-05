process <- function(...) NULL
tracer.emit <- function(...) NULL
tracer.emit(process(value = "hello"))
tracer.emit(process(value = 42))
tracer.emit(process(value = TRUE))
