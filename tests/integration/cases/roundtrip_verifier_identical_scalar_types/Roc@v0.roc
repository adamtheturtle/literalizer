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
    ("value", RList [RBool Bool.true, RBool Bool.false, RInt 0i128, RInt 1i128]),
]
