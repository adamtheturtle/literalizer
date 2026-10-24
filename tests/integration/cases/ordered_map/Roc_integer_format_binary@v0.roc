module [my_data]

Val : [
    RBool Bool,
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("name", RStr "Alice"),
    ("age", RInt 0b11110i128),
    ("active", RBool Bool.true),
]
