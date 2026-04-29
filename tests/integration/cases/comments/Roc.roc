module [my_data]

Val : [
    RBool Bool,
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    # Server configuration
    ("host", RStr "localhost"),  # default host
    ("port", RInt 8080i128),
    # Enable debug mode
    ("debug", RBool Bool.true),
    ]
