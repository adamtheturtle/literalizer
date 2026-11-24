Val := [
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    # outer heading
    # first empty
    RList([]),
    # second empty
    RList([]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
