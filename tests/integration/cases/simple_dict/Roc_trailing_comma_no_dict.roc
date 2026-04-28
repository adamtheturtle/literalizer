module [my_data]

Val : [
    RNull,
    RBool Bool,
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("name", RStr "Alice"),
    ("age", RInt 30),
    ("active", RBool Bool.true),
    ("score", RNull)
    ]
