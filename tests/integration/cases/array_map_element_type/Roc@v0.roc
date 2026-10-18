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
    ("d", RList [RDict [("a", RList [RDict [("b", RList [RInt 1i128, RList [RFloat 2.5, RList [RStr "x", RList [RBool Bool.true]]]])]])]]),
]
