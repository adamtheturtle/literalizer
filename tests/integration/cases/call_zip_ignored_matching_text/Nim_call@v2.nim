proc process[T0](value: T0): int {.discardable.} = 0
process("time.Date(2024, time.January, 15, 12, 0, 0, 0, time.UTC)")
