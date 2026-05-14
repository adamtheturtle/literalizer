module [my_data]

Val : [
    RNull,
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("outer", RDict [("a", RInt 1i128), ("b", RStr "x"), ("c", RNull)]),
    ]
