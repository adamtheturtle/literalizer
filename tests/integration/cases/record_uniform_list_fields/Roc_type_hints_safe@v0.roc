module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RList [
    RDict [("scores", RList [RInt 1i128, RInt 2i128])],
    RDict [("scores", RList [RInt 3i128, RInt 4i128])],
]
