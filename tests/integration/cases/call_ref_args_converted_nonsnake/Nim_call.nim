import json
template process(args: varargs[untyped]) = discard
var myVar = @[
    1,
    2,
    3
]
var myOther = @[
    4,
    5,
    6
]
process(myVar, 42)
process(myOther, 7)
