Val := [
    RNull,
    RList(List(Val)),
]

value : Val
value = RNull
my_data : Val
my_data = RList([
    value,
    value,
    RNull,
])

main! = |_args| {
    _ = my_data
    Ok({})
}
