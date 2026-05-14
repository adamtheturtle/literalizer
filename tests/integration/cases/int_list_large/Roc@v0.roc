module [my_data]

Val : [
    RInt I128,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RInt 1000000i128,
    RInt -1234i128,
    RInt 255i128,
    RInt -10i128,
    ]
