record_value <- function(...) NULL
flush_buffer <- function(...) NULL
emit <- function(...) NULL
emit(record_value(value = 42))
flush_buffer(count = 3)
