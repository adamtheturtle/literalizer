Val := [
    RFloat(F64),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RFloat(1.0e-09.F64),
    RFloat(-1.0e-09.F64),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
