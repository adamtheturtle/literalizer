module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RList [
    RList [RDict [("$ref", RStr "repeated_var")], RInt 1i128],
    RList [RDict [("$ref", RStr "single_var")], RInt 0i128],
    RList [RDict [("$ref", RStr "repeated_var")], RInt 8i128],
    ]
