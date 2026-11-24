template process(args: varargs[untyped]) = discard
var big_list = @[
    "x"
]
process({"m": big_list})
