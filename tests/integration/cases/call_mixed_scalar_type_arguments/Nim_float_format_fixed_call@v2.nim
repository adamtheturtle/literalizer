template capture(args: varargs[untyped]) = discard
capture(NaN, Inf, -Inf, 1.250000, {"year": 2024, "month": 1, "day": 15}, {"year": 2024, "month": 1, "day": 15, "hour": 12, "minute": 34, "second": 56}, "[ordinary text]")
