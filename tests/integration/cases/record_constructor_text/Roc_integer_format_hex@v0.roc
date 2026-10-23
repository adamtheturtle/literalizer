module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("text", RStr "Record0("),
    ("number", RInt 0x1i128),
]
