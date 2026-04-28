module [my_data]

Val : [
    RInt I128,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RList [RList [RInt 1, RInt 2], RList [RInt 3, RInt 4]],
    RList [RList [RInt 5]],
    ]
