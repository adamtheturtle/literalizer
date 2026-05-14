module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("a", RInt 1i128),
    ("b", RInt 3000000000i128),
    ("c", RStr "x"),
    ]
