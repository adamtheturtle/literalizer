proc process[T0](value: T0): int {.discardable.} = 0
proc emit[T1](argument0: int; argument1: T1) = discard
emit(process(1), "2024-01-15T12:00:00")
