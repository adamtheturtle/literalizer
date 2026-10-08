module [my_data]

Val : [
    RInt I128,
    RFloat F64,
    RList (List Val),
]

empty_values : Val
empty_values = RList []
integer_values : Val
integer_values = RList [
    RInt 1i128,
]
float_values : Val
float_values = RList [
    RFloat 1.5,
]
my_data : Val
my_data = RList [
    empty_values,
    integer_values,
    float_values,
]
