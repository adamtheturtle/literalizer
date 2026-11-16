Val := [
    RNull,
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RNull,
])

main! = |_args| {
    _ = my_data
    Ok({})
}
