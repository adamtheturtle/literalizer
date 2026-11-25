Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RList([RInt(1.I128), RInt(2.I128)]),
    RList([RStr("a"), RStr("b")]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
