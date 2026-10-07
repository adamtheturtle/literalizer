module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("plain", RList [RInt 1i128, RInt 2i128]),
    ("with-dash", RStr "a\nb"),
]
