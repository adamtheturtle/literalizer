Val := [
    RInt(I128),
    RFloat(F64),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RInt(-42.I128),
    RInt(0.I128),
    RInt(42.I128),
    RFloat(-1.250000.F64),
    RFloat(0.000000.F64),
    RFloat(1.250000.F64),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
