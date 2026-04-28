module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RList [RList [RInt 1, RInt 2], RList [RStr "a", RStr "b"]],
    ]
