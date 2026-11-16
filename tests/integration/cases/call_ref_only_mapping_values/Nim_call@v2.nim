import json
template consume(args: varargs[untyped]) = discard
var item = %* 42
consume({"field": item})
