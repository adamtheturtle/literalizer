module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("b", RDict [("k", RInt 1i128)]),
    ("a", RDict [("k", RInt 2208988800i128)]),
]
