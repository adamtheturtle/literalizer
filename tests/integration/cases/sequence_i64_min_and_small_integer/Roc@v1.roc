Val := [
    RInt(I128),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RInt(-9223372036854775808.I128),
    RInt(1.I128),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
