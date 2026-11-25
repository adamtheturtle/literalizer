Val := [
    RStr(Str),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RStr("48656c6c6f"),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
