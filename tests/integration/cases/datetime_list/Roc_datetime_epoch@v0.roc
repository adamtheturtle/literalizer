module [my_data]

Val : [
    RInt I128,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RInt 1705321800i128,
    RInt 1717228800i128,
    ]
