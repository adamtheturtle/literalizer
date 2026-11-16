Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RList([
    RDict([("input", RDict([("name", RStr("alice")), ("city", RStr("paris"))])), ("expected", RDict([("count", RInt(1.I128)), ("total", RInt(2.I128))]))]),
    RDict([("input", RDict([("name", RInt(10.I128)), ("city", RInt(20.I128))])), ("expected", RDict([("count", RStr("done")), ("total", RStr("pending"))]))]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
