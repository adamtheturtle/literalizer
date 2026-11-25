Val := [
    RFloat(F64),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RFloat(5.0e-324.F64),
    RFloat(-5.0e-324.F64),
    RFloat(2.2250738585072014e-308.F64),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
