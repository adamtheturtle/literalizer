proc process[T0](value: T0): int {.discardable.} = 0
template emit(args: varargs[untyped]) = discard
emit(process("hello"), {"a": 1, "b": 2})
emit(process(42), {"c": 3, "d": 4})
