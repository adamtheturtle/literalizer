proc process[T0](value: T0): int {.discardable.} = 0
template emit(args: varargs[untyped]) = discard
emit(process(1), {"year": 2024, "month": 1, "day": 15, "hour": 12, "minute": 0, "second": 0})
