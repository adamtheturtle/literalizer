module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RList [
    RDict [("a", RList [RInt 1i128])],
    RDict [("a", RList [RInt 2i128])],
]
