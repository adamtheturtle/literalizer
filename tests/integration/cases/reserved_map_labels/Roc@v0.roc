module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("if", RInt 1i128),
    ("then", RInt 2i128),
    ("else", RInt 3i128),
    ("let", RInt 4i128),
    ("in", RInt 5i128),
    ("using", RInt 6i128),
    ("missing", RInt 7i128),
    ("assert", RInt 8i128),
    ("as", RInt 9i128),
    ("Infinity", RInt 10i128),
    ("NaN", RInt 11i128),
    ("merge", RInt 12i128),
    ("Some", RInt 13i128),
    ("toMap", RInt 14i128),
    ("forall", RInt 15i128),
    ("with", RInt 16i128),
    ("ordinary", RInt 17i128),
]
