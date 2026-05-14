module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("level1", RDict [("level2", RDict [("level3", RDict [("level4", RDict [("value", RStr "deep"), ("items", RList [RStr "a", RStr "b"])])]), ("sibling", RInt 42i128)]), ("tags", RList [RDict [("name", RStr "tag1"), ("meta", RDict [("priority", RInt 1i128), ("labels", RList [RStr "x", RStr "y"])])]])]),
    ]
