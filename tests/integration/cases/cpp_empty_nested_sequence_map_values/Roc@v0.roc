module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("alpha", RList [RInt 2i128, RList []]),
    ("beta", RList [RInt 5i128, RList [RStr "x"]]),
]
