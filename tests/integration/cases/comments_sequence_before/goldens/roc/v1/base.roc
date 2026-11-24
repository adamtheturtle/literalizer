Val := [
    RStr(Str),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    # first
    RStr("a"),
    # second
    RStr("b"),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
