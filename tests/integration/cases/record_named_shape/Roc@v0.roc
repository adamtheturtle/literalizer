module [my_data]

Val : [
    RBool Bool,
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RList [
    RDict [("id", RInt 100i128), ("label", RStr "first item"), ("enabled", RBool Bool.false), ("related_ids", RList [RInt 102i128, RInt 103i128])],
    RDict [("id", RInt 101i128), ("label", RStr "second item"), ("enabled", RBool Bool.true), ("related_ids", RList [RInt 100i128])],
    ]
