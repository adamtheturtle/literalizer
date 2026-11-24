Val := [
    RFloat(F64),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RFloat(-0.0.F64),
    RFloat(1.5.F64),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
