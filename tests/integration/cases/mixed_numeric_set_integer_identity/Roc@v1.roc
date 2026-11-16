Val := [
    RInt(I128),
    RFloat(F64),
    RSet(List(Val)),
]

my_data : Val
my_data = RSet([
    RFloat(1.5.F64),
    RInt(9007199254740993.I128),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
