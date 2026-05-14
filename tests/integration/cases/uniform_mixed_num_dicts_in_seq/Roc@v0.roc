module [my_data]

Val : [
    RInt I128,
    RFloat F64,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RList [
    RDict [("x", RInt 1i128), ("y", RFloat 2.5)],
    RDict [("x", RInt 3i128), ("y", RFloat 4.0)],
    ]
