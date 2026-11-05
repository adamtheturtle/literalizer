import json
template consume(args: varargs[untyped]) = discard
var external_value = %* 1
consume(external_value)
