module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("numbers", RList [RInt 1i128, RInt 2i128]),
    ("nested", RDict [("inner", RList [RInt 3i128])]),
    ("mixed", RList [RInt 4i128, RStr "five"]),
]
