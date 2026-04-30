module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RList [
    RList [RList [RDict [("$ref", RStr "myVar")], RInt 42i128, RStr "static"]],
    ]
