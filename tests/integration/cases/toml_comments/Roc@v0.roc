module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    # before
    ("answer", RInt 42i128),  # inline
    ("plain", RStr "ok"),
    # trailing
    ]
