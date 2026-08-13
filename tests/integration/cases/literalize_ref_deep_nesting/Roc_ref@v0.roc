module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

deep : Val
deep = RList [
    RList [
        RInt 1i128,
        RInt 2i128,
        ],
    RList [
        RInt 3i128,
        RInt 4i128,
        ],
    ]
my_data : Val
my_data = RDict [
    ("a", RDict [
        ("b", RDict [
            ("c", deep),
            ]),
        ]),
    ]
