capture <- function(...) NULL
capture(nan_value = NaN, positive_infinity = Inf, negative_infinity = -Inf, finite_value = 1.25, date_value = as.Date("2024-01-15"), datetime_value = as.POSIXct("2024-01-15 12:34:56", format = "%Y-%m-%d %H:%M:%OS"), text_value = "[ordinary text]")
