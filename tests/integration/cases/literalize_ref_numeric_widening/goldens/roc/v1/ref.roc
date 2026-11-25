Val := [
    RInt(I128),
    RFloat(F64),
    RList(List(Val)),
]

floating_value : Val
floating_value = RFloat(1.5.F64)
integer_value : Val
integer_value = RFloat(2.0.F64)
my_data : Val
my_data = RList([
    floating_value,
    integer_value,
])

main! = |_args| {
    _ = my_data
    Ok({})
}
