module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("single_map", RList [RDict []]),
    ("single_list", RList [RList [RInt 1i128]]),
    ("single_deep", RList [RList [RList [RInt 2i128]]]),
]
