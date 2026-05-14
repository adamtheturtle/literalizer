module [my_data]

Val : [
    RBool Bool,
    RInt I128,
    RFloat F64,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("name", RStr "Alice"),
    ("age", RInt 30i128),
    ("active", RBool Bool.true),
    ("score", RFloat 4.5),
    ]
