module [my_data]

Val : [
    RInt I128,
    RList (List Val),
]

empty_values : Val
empty_values = RList []
integer_values : Val
integer_values = RList [
    RInt 1i128,
]
my_data : Val
my_data = RList [
    empty_values,
    integer_values,
]
