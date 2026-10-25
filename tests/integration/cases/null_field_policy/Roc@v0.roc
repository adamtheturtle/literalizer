module [my_data]

Val : [
    RNull,
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("drop", RNull),
    ("keep", RInt 1i128),
]
