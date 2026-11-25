import json
template f(args: varargs[untyped]) = discard
var ref_data = %* [
    [
        1,
        2
    ],
    [
        3,
        4
    ]
]
f([
    [
        ref_data
    ]
])
