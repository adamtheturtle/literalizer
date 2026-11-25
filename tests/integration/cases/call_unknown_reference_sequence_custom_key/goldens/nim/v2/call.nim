import json
template process(args: varargs[untyped]) = discard
var untypedValue = %* []
process([untypedValue, untypedValue])
