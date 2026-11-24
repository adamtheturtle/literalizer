Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RList([RInt(1.I128), RStr("a")]),
    RList([RInt(2.I128), RStr("b")]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
