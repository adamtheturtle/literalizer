module [my_data]

Val : [
    RInt I128,
    RFloat F64,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("a", RInt 1i128),
    ("b", RFloat 2.5),
    ("c", RInt 3i128),
    ]
