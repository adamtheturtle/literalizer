proc process[T0](value: T0): int {.discardable.} = 0
template emit(args: varargs[untyped]) = discard
emit(process(42), true)
