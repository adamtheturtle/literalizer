Val := [
    RInt(I128),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RInt(0o67405553164730777777.I128),
    RInt(-0o67405553164730777777.I128),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
