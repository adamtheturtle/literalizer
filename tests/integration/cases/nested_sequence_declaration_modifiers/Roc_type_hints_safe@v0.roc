module [my_data]

Val : [
    RNull,
    RBool Bool,
    RInt I128,
    RStr Str,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RList [],
    RList [RInt 1i128],
    RList [RInt 1i128, RInt 2i128],
    RList [RInt 1i128, RStr "x", RBool Bool.true, RNull],
    RList [RInt 1i128, RInt 2i128, RInt 3i128, RInt 4i128, RInt 5i128, RInt 6i128, RInt 7i128, RInt 8i128],
]
