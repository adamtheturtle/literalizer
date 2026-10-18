module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("first", RDict [("items", RList [RInt 1i128, RDict [("value", RInt 2i128)]])]),
    ("second", RDict [("items", RList [RInt 1i128, RDict [("value", RStr "s")]])]),
]
