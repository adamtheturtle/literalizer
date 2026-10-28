module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("below", RInt -0o20000000001i128),
    ("minimum", RInt -0o20000000000i128),
    ("above", RInt -0o17777777777i128),
    ("nested", RList [RInt 0o0i128]),
]
