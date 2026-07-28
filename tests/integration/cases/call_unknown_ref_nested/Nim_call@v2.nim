import json
template process(args: varargs[untyped]) = discard
var known_value = %* true
var unknown_value = %* true
process(known_value, [unknown_value])
