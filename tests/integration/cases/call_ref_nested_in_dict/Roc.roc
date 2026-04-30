module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RList [
    RList [RDict [("key", RDict [("$ref", RStr "my_var")]), ("count", RInt 42i128)]],
    ]
