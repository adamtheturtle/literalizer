Val := [
    RInt(I128),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RInt(-315619200.I128),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
