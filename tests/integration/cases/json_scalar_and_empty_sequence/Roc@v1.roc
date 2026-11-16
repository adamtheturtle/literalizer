Val := [
    RInt(I128),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RInt(1.I128),
    RList([]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
