module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("a", RDict [("k", RInt 1i128)]),
    ("b", RDict [("k", RStr "s")]),
]
