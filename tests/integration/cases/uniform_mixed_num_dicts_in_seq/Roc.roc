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
    RDict [("x", RInt 1), ("y", RFloat 2.5)],
    RDict [("x", RInt 3), ("y", RFloat 4.0)],
    ]
