module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("a-b", RInt 1i128),
    ("a b", RInt 2i128),
    ("a-b-2", RInt 3i128),
]
