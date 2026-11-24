Val := [
    RFloat(F64),
]

my_data : Val
my_data = RFloat(3.140000.F64)

main! = |_args| {
    _ = my_data
    Ok({})
}
