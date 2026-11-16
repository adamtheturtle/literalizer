Val := [
    RStr(Str),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RStr("café"),
    RStr("中文"),
    RStr("😀"),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
