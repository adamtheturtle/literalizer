module [my_data]

Val : [
    RNull,
    RBool Bool,
    RInt I128,
    RFloat F64,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RList [
    RDict [("a", RInt 1i128)],
    RInt 1i128,
    RStr "x",
    RBool Bool.true,
    RFloat 2.5,
    RNull,
]
