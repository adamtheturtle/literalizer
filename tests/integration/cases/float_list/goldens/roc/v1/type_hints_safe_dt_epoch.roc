Val := [
    RFloat(F64),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RFloat(1.1.F64),
    RFloat(-2.2.F64),
    RFloat(3.3.F64),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
