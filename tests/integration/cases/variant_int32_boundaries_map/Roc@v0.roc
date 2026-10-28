module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("below", RInt -2147483649i128),
    ("minimum", RInt -2147483648i128),
    ("above", RInt -2147483647i128),
    ("nested", RList [RInt 0i128]),
]
