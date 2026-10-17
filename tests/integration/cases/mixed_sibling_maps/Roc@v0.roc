module [my_data]

Val : [
    RNull,
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RList [
    RList [RDict [("a", RInt 1i128)], RDict [("a", RNull)], RInt 42i128],
    RList [RDict [("a", RInt 1i128)], RDict [("a", RStr "s")], RInt 42i128],
    RList [RDict [("a", RInt 1i128)], RDict [("a", RNull)]],
    RList [RDict [("a", RInt 1i128)], RDict [("a", RStr "s")]],
]
