module [my_data]

Val : [
    RInt I128,
    RFloat F64,
    RList (List Val),
]

integer_value : Val
integer_value = RFloat 1.0
my_data : Val
my_data = RList [
    integer_value,
    RFloat 1.5,
]
