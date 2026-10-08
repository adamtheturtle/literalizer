module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("astral", RStr "😀"),
    ("mixed", RStr "a😀b"),
    ("count", RInt 2i128),
    ("list", RList [RStr "😀", RInt 1i128]),
    ("nested", RDict [("inner", RStr "😀")]),
]
