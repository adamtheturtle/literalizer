module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RList [
    RDict [("first", RInt 1i128)],
    RDict [("repeated", RStr "a")],
    RDict [("repeated", RStr "b")],
]
