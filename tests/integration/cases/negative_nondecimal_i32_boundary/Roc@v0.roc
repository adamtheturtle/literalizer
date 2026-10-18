module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("minimum", RInt -2147483648i128),
    ("below", RInt -3000000000i128),
]
