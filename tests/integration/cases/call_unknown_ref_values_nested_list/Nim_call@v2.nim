import json
template process(args: varargs[untyped]) = discard
var unknown_value = %* []
process([unknown_value])
