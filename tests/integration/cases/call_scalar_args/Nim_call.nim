import json
proc process(a: varargs[string]) {.used.} = discard
process(value = "hello")
process(value = 42)
process(value = true)
