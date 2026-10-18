module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RList [
    RDict [("k", RInt 2208988800i128)],
    RDict [("k", RInt 1i128)],
]
