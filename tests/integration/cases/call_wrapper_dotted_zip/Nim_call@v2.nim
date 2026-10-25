proc process[T0](value: T0): int {.discardable.} = 0
type HelpersType = object
proc emit[T1](self: HelpersType; argument0: int; argument1: T1) = discard
var helpers: HelpersType
helpers.emit(process(1), 42)
