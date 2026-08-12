module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("a", RDict [
        # inner note
        ("b", RInt 1i128),  # inline b
        ]),
    ("list", RList [
        RInt 1i128,  # first
        RInt 2i128,  # second
        ]),
    ]
