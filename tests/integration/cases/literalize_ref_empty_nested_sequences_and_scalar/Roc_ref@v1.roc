Val := [
    RInt(I128),
    RList(List(Val)),
]

seed : Val
seed = RInt(1.I128)
my_data : Val
my_data = RList([
    RList([]),
    RList([RList([])]),
    seed,
])

main! = |_args| {
    _ = my_data
    Ok({})
}
