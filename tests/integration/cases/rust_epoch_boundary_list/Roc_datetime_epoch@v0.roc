module [my_data]

Val : [
    RInt I128,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RInt -2147483649i128,
    RInt -2147483648i128,
    RInt 2147483647i128,
    RInt 2147483648i128,
]
