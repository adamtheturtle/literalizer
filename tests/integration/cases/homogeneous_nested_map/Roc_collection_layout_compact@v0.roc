module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("first", RDict [("x", RInt 1i128), ("y", RInt 2i128)]),
    ("second", RDict [("z", RInt 3i128)]),
]
