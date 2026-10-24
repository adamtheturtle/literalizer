module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("a", RList [RDict [("item", RList [RInt 1i128])]]),
    ("b", RList [RDict [("item", RList [RInt 2i128])]]),
]
