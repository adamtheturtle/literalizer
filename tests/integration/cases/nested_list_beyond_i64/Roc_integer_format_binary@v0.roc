module [my_data]

Val : [
    RInt I128,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RList [RInt 0b1i128],
    RList [RInt 0b10000000000000000000000000000000000000000000000000000000000000000000000i128],
]
