process <- function(...) NULL
process(value = "09:30:00")
process(value = as.POSIXct("2024-01-15 00:00:00+0000", format = "%Y-%m-%d %H:%M:%OS%z", tz = "UTC"))
process(value = 1)
