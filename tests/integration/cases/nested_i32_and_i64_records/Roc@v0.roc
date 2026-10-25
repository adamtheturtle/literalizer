module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RList [
    RList [RDict [("value", RInt 1i128)]],
    RList [RDict [("value", RInt 1099511627776i128)]],
]
