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
    RDict [("id", RInt 100i128), ("description", RStr "first task"), ("is_done", RBool Bool.false), ("blocks", RList [RInt 102i128, RInt 103i128])],
    RDict [("id", RInt 101i128), ("description", RStr "second task"), ("is_done", RBool Bool.true), ("blocks", RList [RInt 100i128])],
    ]
