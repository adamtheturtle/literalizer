module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("a", RList [RList [RInt 1i128], RList [RInt 2i128]]),
    ("b", RList [RList [RStr "x"], RList [RStr "y"]]),
]
