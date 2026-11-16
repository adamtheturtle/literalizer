Val := [
    RInt(I128),
    RFloat(F64),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RInt(-0x2a.I128),
    RInt(0x0.I128),
    RInt(0x2a.I128),
    RFloat(-1.25.F64),
    RFloat(0.0.F64),
    RFloat(1.25.F64),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
