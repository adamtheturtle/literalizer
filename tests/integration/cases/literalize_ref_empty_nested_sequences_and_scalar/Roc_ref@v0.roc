module [my_data]

Val : [
    RInt I128,
    RList (List Val),
]

seed : Val
seed = RInt 1i128
my_data : Val
my_data = RList [
    RList [],
    RList [RList []],
    seed,
]
