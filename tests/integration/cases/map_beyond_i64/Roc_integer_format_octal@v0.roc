module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("a", RInt 0o777777777777777777777i128),
    ("b", RInt 0o1000000000000000000000i128),
]
