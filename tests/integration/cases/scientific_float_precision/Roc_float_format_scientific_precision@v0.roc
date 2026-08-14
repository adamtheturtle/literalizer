module [my_data]

Val : [
    RFloat F64,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("value", RFloat 1.2345678901234567),
    ]
