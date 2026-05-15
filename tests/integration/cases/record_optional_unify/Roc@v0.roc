module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("items", RList [RDict [("id", RInt 1i128)], RDict [("id", RInt 2i128), ("count", RInt 10i128)], RDict [("id", RInt 3i128), ("count", RInt 20i128)]]),
    ]
