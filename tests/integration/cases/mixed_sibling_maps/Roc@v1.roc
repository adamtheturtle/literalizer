Val := [
    RNull,
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RList([
    RList([RDict([("a", RInt(1.I128))]), RDict([("a", RNull)]), RInt(42.I128)]),
    RList([RDict([("a", RInt(1.I128))]), RDict([("a", RStr("s"))]), RInt(42.I128)]),
    RList([RDict([("a", RInt(1.I128))]), RDict([("a", RNull)])]),
    RList([RDict([("a", RInt(1.I128))]), RDict([("a", RStr("s"))])]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
