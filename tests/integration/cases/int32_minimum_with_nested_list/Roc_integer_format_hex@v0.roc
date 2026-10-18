module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("minimum", RInt -0x80000000i128),
    ("neighbor", RInt -0x7fffffffi128),
    ("maximum", RInt 0x7fffffffi128),
    ("nested", RList [RInt -0x80000000i128]),
]
