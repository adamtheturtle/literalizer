module [my_data]

Val : [
    RBool Bool,
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("h", RList [RInt 1i128, RStr "a", RList [RInt 2i128, RStr "b"], RDict [("k", RList [RBool Bool.true])]]),
]
