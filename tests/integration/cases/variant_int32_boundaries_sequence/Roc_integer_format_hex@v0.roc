module [my_data]

Val : [
    RInt I128,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RInt -0x80000000i128,
    RInt -0x7fffffffi128,
    RList [RInt 0x0i128],
]
