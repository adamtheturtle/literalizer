Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("lists", RList([RList([RInt(1.I128)]), RList([RStr("x")]), RList([])])),
    ("maps", RList([RDict([("x", RInt(1.I128))]), RDict([("x", RStr("s"))])])),
    ("empties", RDict([("a", RList([RInt(1.I128)])), ("b", RList([]))])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
