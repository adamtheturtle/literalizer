Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RList([
    RDict([("a\tb\nc", RInt(1.I128)), ("id", RStr("x"))]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
