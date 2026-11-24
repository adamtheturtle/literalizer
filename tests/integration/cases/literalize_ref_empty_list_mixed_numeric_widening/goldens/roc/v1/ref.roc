Val := [
    RInt(I128),
    RFloat(F64),
    RList(List(Val)),
]

empty_values : Val
empty_values = RList([])
integer_values : Val
integer_values = RList([
    RInt(1.I128),
])
float_values : Val
float_values = RList([
    RFloat(1.5.F64),
])
my_data : Val
my_data = RList([
    empty_values,
    integer_values,
    float_values,
])

main! = |_args| {
    _ = my_data
    Ok({})
}
