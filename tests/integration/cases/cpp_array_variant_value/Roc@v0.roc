module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("a", RInt 1i128),
    ("b", RStr "x"),
    ("e", RList [RInt 1i128, RInt 2i128]),
    ("f", RDict [("g", RStr "h")]),
]
