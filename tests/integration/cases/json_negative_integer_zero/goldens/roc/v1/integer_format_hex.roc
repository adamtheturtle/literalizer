Val := [
    RFloat(F64),
]

my_data : Val
my_data = RFloat(-0.0.F64)

main! = |_args| {
    _ = my_data
    Ok({})
}
