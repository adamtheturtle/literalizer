module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RList [
    RList [RDict [("a", RInt 1i128)]],
    RList [RDict [("a", RInt 2i128)]],
]
