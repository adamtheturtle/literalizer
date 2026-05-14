module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("id", RInt 1i128),
    ("owner", RDict [("name", RStr "Alice"), ("age", RInt 30i128)]),
    ]
