proc process[T0](value: T0): int {.discardable.} = 0
template emit(args: varargs[untyped]) = discard
emit(process("hello"), 1)
emit(process(42), 0)
