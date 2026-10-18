module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("minimum", RInt -0o20000000000i128),
    ("below", RInt -0o26264057000i128),
]
