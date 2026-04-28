module [my_data]

Val : [
    RInt I128,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RInt 1000000,
    RInt -1234,
    RInt 255,
    RInt -10,
    ]
