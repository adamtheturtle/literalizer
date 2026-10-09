template f(args: varargs[untyped]) = discard
var ref_data = @[
    1,
    2
]
f([
    ref_data
])
f([
    ref_data
])
