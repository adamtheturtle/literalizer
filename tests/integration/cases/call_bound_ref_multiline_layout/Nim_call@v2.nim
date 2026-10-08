import json
template f(args: varargs[untyped]) = discard
var x = %* [
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
        x
    ]
])
