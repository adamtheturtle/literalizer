Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RList([
    RDict([("k", RInt(2208988800.I128))]),
    RDict([("k", RInt(1.I128))]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
