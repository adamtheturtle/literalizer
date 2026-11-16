Val := [
    RInt(I128),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RInt(-0b10000000000000000000000000000000.I128),
    RInt(-0b1111111111111111111111111111111.I128),
    RList([RInt(0b0.I128)]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
