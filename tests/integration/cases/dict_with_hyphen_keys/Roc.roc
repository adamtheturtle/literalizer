module [my_data]

Val : [
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("my-key", RStr "value1"),
    ("another-key", RStr "value2"),
    ("normal_key", RStr "value3"),
    ]
