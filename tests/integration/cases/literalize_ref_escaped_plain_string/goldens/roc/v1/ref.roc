Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RInt(0.I128),
    RList([RList([RStr("plain")])]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
