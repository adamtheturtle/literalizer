Val := [
    RFloat(F64),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RList([RFloat(1.5.F64), RFloat(2.5.F64)]),
    RList([RFloat(3.5.F64), RFloat(4.5.F64)]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
