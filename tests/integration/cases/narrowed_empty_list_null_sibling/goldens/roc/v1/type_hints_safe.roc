Val := [
    RNull,
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RList([RNull]),
    RList([]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
