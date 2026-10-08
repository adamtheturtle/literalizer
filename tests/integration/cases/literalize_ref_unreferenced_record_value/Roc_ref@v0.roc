module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

other : Val
other = RStr "true"
my_data : Val
my_data = RDict [
    ("main", RDict [("x", RInt 1i128), ("y", RStr "s")]),
]
