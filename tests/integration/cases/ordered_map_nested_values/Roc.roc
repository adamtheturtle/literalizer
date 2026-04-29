module [my_data]

Val : [
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("name", RStr "Alice"),
    ("scores", RDict [("1", RStr "first"), ("2", RStr "second")]),
    ]
