module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

sibling_map : Val
sibling_map = RDict [
    ("k", RInt 2i128),
]
my_data : Val
my_data = RList [
    RDict [("k", RInt 1i128)],
    sibling_map,
]
