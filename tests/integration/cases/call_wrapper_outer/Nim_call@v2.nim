proc process[T0](value: T0): int {.discardable.} = 0
proc emit(argument0: int) = discard
emit(process(42))
