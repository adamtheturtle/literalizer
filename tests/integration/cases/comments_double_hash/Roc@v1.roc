Val := [
    RStr(Str),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    # # section
    RStr("a"),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
