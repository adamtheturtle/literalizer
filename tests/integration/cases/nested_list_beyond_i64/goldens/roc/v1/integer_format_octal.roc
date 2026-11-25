Val := [
    RInt(I128),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RList([RInt(0o1.I128)]),
    RList([RInt(0o200000000000000000000000.I128)]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
