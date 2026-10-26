module [my_data]

Val : [
    RBool Bool,
    RInt I128,
    RFloat F64,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("below", RList [RList [RList [RList [RList [RList [RList [RList [RInt 1i128]]]]]]]]),
    ("boundary", RList [RList [RList [RList [RList [RList [RList [RList [RList [RInt 2i128]]]]]]]]]),
    ("multiple", RList [RList [RList [RList [RList [RList [RList [RList [RList [RList [RList [RList [RList [RList [RList [RList [RList [RInt 3i128]]]]]]]]]]]]]]]]]),
    ("text", RList [RList [RList [RList [RList [RList [RList [RList [RList [RStr "value"]]]]]]]]]),
    ("boolean", RList [RList [RList [RList [RList [RList [RList [RList [RList [RBool Bool.true]]]]]]]]]),
    ("float", RList [RList [RList [RList [RList [RList [RList [RList [RList [RFloat 1.5]]]]]]]]]),
]
