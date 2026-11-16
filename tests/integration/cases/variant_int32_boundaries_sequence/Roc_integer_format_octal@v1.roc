Val := [
    RInt(I128),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RInt(-0o20000000000.I128),
    RInt(-0o17777777777.I128),
    RList([RInt(0o0.I128)]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
