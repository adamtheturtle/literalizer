module [my_data]

Val : [
    RInt I128,
    RFloat F64,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("_", RList [RInt 1i128, RFloat 2.5, RInt 3i128]),
]
