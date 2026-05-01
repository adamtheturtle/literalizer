import json
template send(args: varargs[untyped]) = discard
var existing = %* 42
send(existing)
