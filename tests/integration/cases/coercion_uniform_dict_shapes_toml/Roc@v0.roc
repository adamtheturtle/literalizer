module [my_data]

Val : [
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("_", RList [RDict [("type", RStr "create"), ("name", RStr "a")], RDict [("type", RStr "update"), ("name", RStr "b")]]),
]
