Val := [
    RStr(Str),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RStr("a"),  # note a
    RStr("b"),  # note b
])

main! = |_args| {
    _ = my_data
    Ok({})
}
