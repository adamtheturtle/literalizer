Val := [
    RFloat(F64),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RFloat(1.100000.F64),
    RFloat(-2.200000.F64),
    RFloat(3.300000.F64),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
