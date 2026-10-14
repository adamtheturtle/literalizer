module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("below", RInt -0b10000000000000000000000000000001i128),
    ("minimum", RInt -0b10000000000000000000000000000000i128),
    ("above", RInt -0b1111111111111111111111111111111i128),
    ("nested", RList [RInt 0b0i128]),
]
