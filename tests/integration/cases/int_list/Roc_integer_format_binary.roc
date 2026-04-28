module [my_data]

Val : [
    RInt I128,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RInt 0b1,
    RInt 0b10,
    RInt 0b11,
    ]
