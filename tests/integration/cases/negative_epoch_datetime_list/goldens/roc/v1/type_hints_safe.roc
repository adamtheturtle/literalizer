Val := [
    RStr(Str),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RStr("1960-01-01T00:00:00+00:00"),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
