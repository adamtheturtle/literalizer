module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("minimum", RInt -0b10000000000000000000000000000000i128),
    ("neighbor", RInt -0b1111111111111111111111111111111i128),
    ("maximum", RInt 0b1111111111111111111111111111111i128),
    ("nested", RList [RInt -0b10000000000000000000000000000000i128]),
]
