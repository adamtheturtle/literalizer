Val := [
    RInt(I128),
    RFloat(F64),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RInt(-0o52.I128),
    RInt(0o0.I128),
    RInt(0o52.I128),
    RFloat(-1.25.F64),
    RFloat(0.0.F64),
    RFloat(1.25.F64),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
