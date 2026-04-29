proc process[T0](value: T0): int {.discardable.} = 0
process("hello")
process(42)
process(true)
