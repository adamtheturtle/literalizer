module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("rows", RList [RDict [("x", RInt 1i128), ("y", RStr "a")], RDict [("x", RInt 2i128), ("y", RStr "b")]]),
]
