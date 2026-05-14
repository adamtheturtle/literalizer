module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("metrics", RDict [("count", RInt 100i128), ("rate", RInt 50i128)]),
    ("flags", RDict [("retries", RInt 3i128), ("timeout", RInt 30i128)]),
    ]
