module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("a", RList [
        RInt 1i128,
        RInt 2i128,
        RInt 3i128,
        ]),  # inline a
    ("b", RInt 2i128),  # inline b
    ]
