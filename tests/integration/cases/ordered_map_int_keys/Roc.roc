module [my_data]

Val : [
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("1", RStr "one"),
    ("2", RStr "two"),
    ("42", RStr "answer"),
    ]
