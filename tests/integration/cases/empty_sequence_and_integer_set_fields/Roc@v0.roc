module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
    RSet (List Val),
]

my_data : Val
my_data = RDict [
    ("a", RList []),
    ("b", RSet [RInt 1i128, RInt 2i128]),
]
