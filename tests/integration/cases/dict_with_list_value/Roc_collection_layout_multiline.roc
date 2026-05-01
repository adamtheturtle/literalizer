module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("name", RStr "Alice"),
    ("scores", RList [
        RInt 10i128,
        RInt 20i128,
        RInt 30i128,
        ]),
    ]
