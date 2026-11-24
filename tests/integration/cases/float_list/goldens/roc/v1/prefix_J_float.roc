Val := [
    JFloat(F64),
    JList(List(Val)),
]

my_data : Val
my_data = JList([
    JFloat(1.1.F64),
    JFloat(-2.2.F64),
    JFloat(3.3.F64),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
