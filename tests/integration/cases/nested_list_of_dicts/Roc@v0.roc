module [my_data]

Val : [
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RList [
    RList [RDict [("name", RStr "Alice")], RDict [("name", RStr "Bob")]],
    RList [RDict [("name", RStr "Charlie")], RDict [("name", RStr "Dave")]],
    ]
