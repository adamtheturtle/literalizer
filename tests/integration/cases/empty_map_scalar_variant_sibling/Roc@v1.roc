Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RList([
    RDict([("count", RInt(1.I128)), ("name", RStr("value"))]),
    RDict([]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
