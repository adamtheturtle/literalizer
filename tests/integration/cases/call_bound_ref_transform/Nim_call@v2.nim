import json
proc f[T0](a: T0): int {.discardable.} = 0
var ref_data = %* 1
f(ref_data)
