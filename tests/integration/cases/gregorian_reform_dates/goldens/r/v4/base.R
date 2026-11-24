my_data <- list(
    "ancient_date" = as.Date("1500-03-01"),
    "modern_date" = as.Date("2024-01-15"),
    "before_date" = as.Date("1582-10-04"),
    "gap_date" = as.Date("1582-10-10"),
    "transition_date" = as.Date("1582-10-15"),
    "after_date" = as.Date("1582-10-16"),
    "before_naive" = as.POSIXct("1582-10-04 12:30:00.000001", format = "%Y-%m-%d %H:%M:%OS"),
    "gap_naive" = as.POSIXct("1582-10-10 12:30:00.500000", format = "%Y-%m-%d %H:%M:%OS"),
    "transition_positive" = as.POSIXct("1582-10-14 06:30:00+0000", format = "%Y-%m-%d %H:%M:%OS%z", tz = "UTC"),
    "transition_negative" = as.POSIXct("1582-10-16 17:30:00+0000", format = "%Y-%m-%d %H:%M:%OS%z", tz = "UTC"),
    "after_positive" = as.POSIXct("1582-10-15 06:30:00+0000", format = "%Y-%m-%d %H:%M:%OS%z", tz = "UTC")
)
