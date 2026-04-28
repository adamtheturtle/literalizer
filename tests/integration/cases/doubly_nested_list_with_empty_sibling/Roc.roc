module [my_data]

Val : [
    RInt I128,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RList [RList [RInt 1i128, RInt 2i128]],
    RList [],
    RList [RList [RInt 3i128, RInt 4i128]],
    ]
