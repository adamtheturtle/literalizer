import json
template process(args: varargs[untyped]) = discard
var myVar = @[
    1,
    2,
    3
]
process(myVar)
