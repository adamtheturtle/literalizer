module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("a", RList [RDict [], RDict [("x", RInt 1i128)]]),
    ("b", RList [RList [], RList [RInt 1i128]]),
]
