Val := [
    RFloat(F64),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RFloat(0.0.F64),
    RFloat(1.0.F64),
    RFloat(1.5e3.F64),
    RFloat(1.0e-3.F64),
    RFloat(1.0e16.F64),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
