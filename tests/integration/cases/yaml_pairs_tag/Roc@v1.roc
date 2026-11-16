Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RList([
    RDict([("first", RInt(1.I128))]),
    RDict([("repeated", RStr("a"))]),
    RDict([("repeated", RStr("b"))]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
