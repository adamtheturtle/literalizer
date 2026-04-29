module [my_data]

Val : [
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RList [
    RDict [("first", RStr "Alice"), ("last", RStr "Smith")],
    RDict [("first", RStr "Bob"), ("last", RStr "Jones")],
    ]
