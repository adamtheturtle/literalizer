Val := [
    RStr(Str),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RStr("foo"),
    RStr("bar"),
    RStr("baz"),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
