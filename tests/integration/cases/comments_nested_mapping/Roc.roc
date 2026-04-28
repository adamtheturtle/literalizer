module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("a", RDict [("x", RInt 1)]),
    ("b", RInt 2),
    ]
