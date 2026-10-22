module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RList [],
    RList [RInt 1i128, RStr "value"],
    RList [RInt 2i128, RStr "other"],
]
