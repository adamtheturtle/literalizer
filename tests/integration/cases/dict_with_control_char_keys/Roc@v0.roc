module [my_data]

Val : [
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("key\nwith\nnewlines", RStr "value1"),
    ("key\twith\ttabs", RStr "value2"),
    ("", RStr "value3"),
    ]
