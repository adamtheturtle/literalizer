proc record_value[T0](value: T0): int {.discardable.} = 0
template flush_buffer(args: varargs[untyped]) = discard
template emit(args: varargs[untyped]) = discard
emit(record_value(42))
flush_buffer(3)
