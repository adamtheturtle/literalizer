module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("lower", RInt 3735928559i128),
    ("upper", RInt 31i128),
    ("negative", RInt -16i128),
    ("zero", RInt 0i128),
]
