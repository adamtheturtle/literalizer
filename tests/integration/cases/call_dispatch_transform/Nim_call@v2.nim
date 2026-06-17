proc record[T0](value: T0): int {.discardable.} = 0
template flush(args: varargs[untyped]) = discard
record(42)
flush(3)
