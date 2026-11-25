Val := [
    RInt(I128),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RInt(-2147483648.I128),
    RInt(-2147483647.I128),
    RList([RInt(0.I128)]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
