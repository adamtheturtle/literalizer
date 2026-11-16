Val := [
    RFloat(F64),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RFloat(5.0e-324.F64),
    RFloat(-5.0e-324.F64),
    RFloat(1.0e-310.F64),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
