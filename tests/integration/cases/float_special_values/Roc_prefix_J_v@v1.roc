Val := [
    JFloat(F64),
    JList(List(Val)),
]

my_data : Val
my_data = JList([
    JFloat(F64.infinity),
    JFloat(-F64.infinity),
    JFloat(F64.nan),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
