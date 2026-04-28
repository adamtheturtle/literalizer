process <- function(...) NULL
log.emit <- function(...) NULL
log.emit(process(value = "hello"))
log.emit(process(value = 42))
log.emit(process(value = TRUE))
