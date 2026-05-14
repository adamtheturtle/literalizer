module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("user", RDict [("id", RInt 1i128), ("name", RStr "Alice")]),
    ("project", RDict [("title", RStr "report"), ("tags", RList [RStr "draft", RStr "urgent"])]),
    ]
