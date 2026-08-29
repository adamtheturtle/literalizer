template process(args: varargs[untyped]) = discard
var big_list = @[
    "x"
]
process({"k": big_list}, {"m": big_list})
