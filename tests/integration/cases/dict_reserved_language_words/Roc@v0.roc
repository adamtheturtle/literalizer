module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("assert", RInt 1i128),
    ("else", RInt 1i128),
    ("error", RInt 1i128),
    ("false", RInt 1i128),
    ("for", RInt 1i128),
    ("function", RInt 1i128),
    ("if", RInt 1i128),
    ("import", RInt 1i128),
    ("importbin", RInt 1i128),
    ("importstr", RInt 1i128),
    ("in", RInt 1i128),
    ("local", RInt 1i128),
    ("null", RInt 1i128),
    ("self", RInt 1i128),
    ("super", RInt 1i128),
    ("tailstrict", RInt 1i128),
    ("then", RInt 1i128),
    ("true", RInt 1i128),
    ("ordinary", RInt 1i128),
    ]
