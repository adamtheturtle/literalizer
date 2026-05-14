module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RList [
    RDict [("id", RInt 1i128), ("label", RStr "first")],
    RDict [("id", RInt 2i128), ("label", RStr "second")],
    RDict [("id", RInt 3i128), ("label", RStr "third")],
    ]
