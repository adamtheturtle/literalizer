Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("items", RList([RDict([("id", RInt(1.I128))]), RDict([("id", RInt(2.I128)), ("count", RInt(10.I128))]), RDict([("id", RInt(3.I128)), ("count", RInt(20.I128))])])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
