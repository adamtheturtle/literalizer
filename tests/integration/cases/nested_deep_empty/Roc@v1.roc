Val := [
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RList([RList([]), RList([])]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
