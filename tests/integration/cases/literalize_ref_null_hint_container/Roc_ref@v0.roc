module [my_data]

Val : [
    RNull,
    RInt I128,
    RList (List Val),
]

my_value : Val
my_value = RList [
    RInt 1i128,
    RInt 2i128,
]
my_data : Val
my_data = my_value
