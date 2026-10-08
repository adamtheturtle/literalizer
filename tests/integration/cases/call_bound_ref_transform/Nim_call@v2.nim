import json
proc f[T0](a: T0): int {.discardable.} = 0
var x = %* 1
f(x)
