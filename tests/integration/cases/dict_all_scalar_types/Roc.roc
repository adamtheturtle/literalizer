module [my_data]

Val : [
    RNull,
    RBool Bool,
    RInt I128,
    RFloat F64,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("s", RStr "string"),
    ("i", RInt 1i128),
    ("f", RFloat 1.5),
    ("b", RBool Bool.true),
    ("n", RNull),
    ("d", RStr "2024-01-15"),
    ("dt", RStr "2024-01-15T12:00:00"),
    ("by", RStr "48656c6c6f"),
    ]
