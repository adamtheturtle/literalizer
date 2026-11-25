Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RList([
    RDict([("k", RStr("2040-01-01T00:00:00+00:00"))]),
    RDict([("k", RInt(1.I128))]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
