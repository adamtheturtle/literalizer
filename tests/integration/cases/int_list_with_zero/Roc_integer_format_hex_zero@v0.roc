module [my_data]

Val : [
    RInt I128,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RInt 0x0i128,
    RInt 0x1i128,
    RInt -0x1i128,
    ]
