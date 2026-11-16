Val := [
    RFloat(F64),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RFloat(-0.000000.F64),
    RFloat(1.500000.F64),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
