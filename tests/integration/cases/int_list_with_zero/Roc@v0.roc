module [my_data]

Val : [
    RInt I128,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RInt 0i128,
    RInt 1i128,
    RInt -1i128,
    ]
