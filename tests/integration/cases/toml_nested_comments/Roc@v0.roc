module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    # About the first dotted key.
    # About the second dotted key.
    ("dotted", RDict [("first", RInt 1i128), ("second", RInt 2i128)]),
    ("plain", RInt 3i128),  # About the plain key.
    # Before the first entry.
    # Before the second entry.
    ("entries", RList [RDict [("name", RStr "one")], RDict [("name", RStr "two")]]),
    # Inside the table.
    ("table", RDict [("inner", RInt 4i128)]),
    ]
