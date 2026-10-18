module [my_data]

Val : [
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("a", RDict [("k", RStr "2020-01-01")]),
    ("b", RDict [("k", RStr "string")]),
]
