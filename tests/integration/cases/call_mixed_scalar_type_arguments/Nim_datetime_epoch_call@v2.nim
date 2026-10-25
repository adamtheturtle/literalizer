template capture(args: varargs[untyped]) = discard
capture(NaN, Inf, -Inf, 1.25, {"year": 2024, "month": 1, "day": 15}, 1705322096, "[ordinary text]")
