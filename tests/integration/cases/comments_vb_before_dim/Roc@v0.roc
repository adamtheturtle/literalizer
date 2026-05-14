module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    # Configuration
    ("name", RStr "app"),
    # Port setting
    ("port", RInt 3000i128),
    ]
