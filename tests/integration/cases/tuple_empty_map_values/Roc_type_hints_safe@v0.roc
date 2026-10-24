module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("filled", RList [RInt 1i128, RStr "value"]),
    ("empty", RList []),
]
