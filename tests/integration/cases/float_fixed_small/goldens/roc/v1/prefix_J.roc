Val := [
    JFloat(F64),
    JList(List(Val)),
]

my_data : Val
my_data = JList([
    JFloat(1.0e-09.F64),
    JFloat(-1.0e-09.F64),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
