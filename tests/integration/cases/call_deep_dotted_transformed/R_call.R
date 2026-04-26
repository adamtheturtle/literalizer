app.client.fetch <- function(...) NULL
emit <- function(...) NULL
emit(app.client.fetch(payload = "hello"))
emit(app.client.fetch(payload = 42))
emit(app.client.fetch(payload = TRUE))
