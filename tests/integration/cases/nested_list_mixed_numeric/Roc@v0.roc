module [my_data]

Val : [
    RInt I128,
    RFloat F64,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RList [RInt 1i128],
    RList [RFloat 2.5],
]
