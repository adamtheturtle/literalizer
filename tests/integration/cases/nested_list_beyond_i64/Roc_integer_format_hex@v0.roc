module [my_data]

Val : [
    RInt I128,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RList [RInt 0x1i128],
    RList [RInt 0x400000000000000000i128],
]
