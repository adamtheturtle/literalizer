module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("below", RInt -0x80000001i128),
    ("minimum", RInt -0x80000000i128),
    ("above", RInt -0x7fffffffi128),
    ("nested", RList [RInt 0x0i128]),
]
