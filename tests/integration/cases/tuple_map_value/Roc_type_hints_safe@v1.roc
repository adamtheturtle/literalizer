Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("rows", RList([RDict([("x", RInt(1.I128)), ("y", RStr("a"))]), RDict([("x", RInt(2.I128)), ("y", RStr("b"))])])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
