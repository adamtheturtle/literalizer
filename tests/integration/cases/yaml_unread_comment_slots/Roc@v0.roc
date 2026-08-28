module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("flow", RList [
        RInt 1i128,
        # After the first element.
        RInt 2i128,
        ]),
    # Between the key and its value.
    ("gap", RInt 3i128),
    # On the block scalar header.
    ("block", RStr "Text.\n"),
    ("nested", RList [
        RInt 1i128,
        RInt 1i128,
        # On the nested alias.
        ]),
    ("anchored", RInt 4i128),
    ("alias", RInt 4i128),
    # On the alias.
    ]
