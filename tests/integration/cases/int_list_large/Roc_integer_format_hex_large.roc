module [my_data]

Val : [
    RInt I128,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RInt 0xf4240,
    RInt -0x4d2,
    RInt 0xff,
    RInt -0xa,
    ]
