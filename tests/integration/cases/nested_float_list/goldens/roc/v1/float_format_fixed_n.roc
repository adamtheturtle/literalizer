Val := [
    RFloat(F64),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RList([RFloat(1.500000.F64), RFloat(2.500000.F64)]),
    RList([RFloat(3.500000.F64), RFloat(4.500000.F64)]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
