Val := [
    RInt(I128),
    RSet(List(Val)),
]

my_data : Val
my_data = RSet([
    RInt(0x1.I128),
    RInt(0x10000000000.I128),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
