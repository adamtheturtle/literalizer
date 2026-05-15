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
    ("quantity", RInt 1000000i128),
    ("big", RInt 18446744073709551615i128),
    ("ratio", RFloat 2.5),
    ("label", RStr "tag"),
    ("ok", RBool Bool.true),
    ]
