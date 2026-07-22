module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RList [
    RDict [("missing", RInt -1i128), ("present", RInt 1i128)],
    RDict [("missing", RInt 2i128), ("present", RInt 3i128)],
    ]
