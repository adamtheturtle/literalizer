Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RList([
    RDict([("name", RStr("Alice")), ("age", RInt(30.I128))]),
    RDict([("name", RStr("Bob")), ("age", RInt(25.I128))]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
