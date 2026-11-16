Val := [
    JInt(I128),
    JFloat(F64),
    JList(List(Val)),
]

my_data : Val
my_data = JList([
    JInt(-42.I128),
    JInt(0.I128),
    JInt(42.I128),
    JFloat(-1.25.F64),
    JFloat(0.0.F64),
    JFloat(1.25.F64),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
