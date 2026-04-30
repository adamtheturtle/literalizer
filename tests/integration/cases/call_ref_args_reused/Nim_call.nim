import json
template process(args: varargs[untyped]) = discard
var repeated_var = %* 1
var single_var = @[
    4,
    5,
    6
]
process(repeated_var, 1)
process(single_var, 0)
process(repeated_var, 8)
