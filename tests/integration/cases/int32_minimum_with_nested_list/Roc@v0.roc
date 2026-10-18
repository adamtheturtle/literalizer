module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("minimum", RInt -2147483648i128),
    ("neighbor", RInt -2147483647i128),
    ("maximum", RInt 2147483647i128),
    ("nested", RList [RInt -2147483648i128]),
]
