import json
template process(args: varargs[untyped]) = discard
var my_int = %* 1
var my_bool = %* true
var my_float = %* 3.14
var my_list = @[
    1,
    2,
    3
]
process(my_int, 42)
process(my_bool, 7)
process(my_float, 9)
process(my_list, 1)
