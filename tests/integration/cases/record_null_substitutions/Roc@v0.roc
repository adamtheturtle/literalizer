module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("rows", RList [RDict [("replacement", RInt -1i128), ("present", RInt 1i128)], RDict [("replacement", RInt 2i128), ("present", RInt 3i128)]]),
    ]
