module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("groups", RList [RList [RDict [("id", RInt 1i128)]], RList [RDict [("id", RInt 2i128)]]]),
]
