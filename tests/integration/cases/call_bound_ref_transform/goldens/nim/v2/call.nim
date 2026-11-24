import json
proc f[T0](a: T0): int {.discardable.} = 0
proc repr(argument0: int) = discard
var ref_data = %* 1
repr(f(ref_data))
