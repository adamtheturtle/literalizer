module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("within_i32", RInt 1705320000i128),
    ("beyond_i32", RInt 4085195400i128),
]
