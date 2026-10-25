module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("lists", RList [RList [RInt 1i128], RList [RStr "x"], RList []]),
    ("maps", RList [RDict [("x", RInt 1i128)], RDict [("x", RStr "s")]]),
    ("empties", RDict [("a", RList [RInt 1i128]), ("b", RList [])]),
]
