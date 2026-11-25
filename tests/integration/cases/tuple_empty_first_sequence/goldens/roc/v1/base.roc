Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RList([]),
    RList([RInt(1.I128), RStr("value")]),
    RList([RInt(2.I128), RStr("other")]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
