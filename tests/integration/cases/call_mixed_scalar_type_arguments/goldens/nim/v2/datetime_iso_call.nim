template capture(args: varargs[untyped]) = discard
capture(NaN, Inf, -Inf, 1.25, {"year": 2024, "month": 1, "day": 15}, "2024-01-15T12:34:56", "[ordinary text]")
