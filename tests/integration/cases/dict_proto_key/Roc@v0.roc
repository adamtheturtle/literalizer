module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("__proto__", RDict [("x", RInt 1i128)]),
    ("n", RDict [("__proto__", RInt 3i128)]),
    ("y", RInt 2i128),
]
