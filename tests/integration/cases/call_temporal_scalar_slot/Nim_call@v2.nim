template process(args: varargs[untyped]) = discard
process("09:30:00")
process({"year": 2024, "month": 1, "day": 15, "hour": 0, "minute": 0, "second": 0})
process(1)
