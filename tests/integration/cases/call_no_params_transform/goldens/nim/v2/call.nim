proc process(): int {.discardable.} = 0
template emit(args: varargs[untyped]) = discard
emit(process())
emit(process())
