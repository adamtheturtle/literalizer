Val := [
    RInt(I128),
    RSet(List(Val)),
]

my_data : Val
my_data = RSet([
    RInt(-1.I128),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
