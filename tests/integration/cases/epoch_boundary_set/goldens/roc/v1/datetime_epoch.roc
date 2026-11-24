Val := [
    RInt(I128),
    RSet(List(Val)),
]

my_data : Val
my_data = RSet([
    RInt(-2147483649.I128),
    RInt(-2147483648.I128),
    RInt(2147483647.I128),
    RInt(2147483648.I128),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
