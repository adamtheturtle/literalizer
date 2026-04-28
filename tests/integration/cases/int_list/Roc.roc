module [my_data]

Val : [
    RInt I128,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RInt 1,
    RInt 2,
    RInt 3,
    ]
