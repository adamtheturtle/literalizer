module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RList [RInt 1i128, RStr "a"],
    RList [RInt 2i128, RStr "b"],
    ]
