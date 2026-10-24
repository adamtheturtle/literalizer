module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("test", RList [RInt 5i128, RList [RStr "compile", RStr "test"]]),
    ("package", RList [RInt 7i128, RList [RStr "link", RStr "test"]]),
]
