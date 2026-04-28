module [my_data]

Val : [
    RInt I128,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RInt 0xf4240i128,
    RInt -0x4d2i128,
    RInt 0xffi128,
    RInt -0xai128,
    ]
