module [my_data]

Val : [
    RInt I128,
    RFloat F64,
    RList (List Val),
]

floating_value : Val
floating_value = RFloat 1.5
integer_value : Val
integer_value = RFloat 2.0
my_data : Val
my_data = RList [
    floating_value,
    integer_value,
]
