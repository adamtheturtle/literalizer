Val := [
    JFloat(F64),
    JList(List(Val)),
]

my_data : Val
my_data = JList([
    JFloat(-0.0.F64),
    JFloat(0.0.F64),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
