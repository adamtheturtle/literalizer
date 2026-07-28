import json
template process(args: varargs[untyped]) = discard
var known_value = %* 1
var unknown_value = %* []
process(unknown_value)
