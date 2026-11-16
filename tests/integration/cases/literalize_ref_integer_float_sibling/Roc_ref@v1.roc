Val := [
    RInt(I128),
    RFloat(F64),
    RList(List(Val)),
]

integer_value : Val
integer_value = RFloat(1.0.F64)
my_data : Val
my_data = RList([
    integer_value,
    RFloat(1.5.F64),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
