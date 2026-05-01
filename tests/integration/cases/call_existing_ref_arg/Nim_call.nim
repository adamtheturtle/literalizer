import json
template process(args: varargs[untyped]) = discard
var existing = %* 42
process(existing)
