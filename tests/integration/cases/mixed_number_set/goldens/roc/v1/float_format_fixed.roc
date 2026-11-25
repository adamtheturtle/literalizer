Val := [
    RInt(I128),
    RFloat(F64),
    RSet(List(Val)),
]

my_data : Val
my_data = RSet([
    RFloat(2.500000.F64),
    RInt(1.I128),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
