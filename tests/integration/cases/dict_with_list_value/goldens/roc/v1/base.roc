Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("name", RStr("Alice")),
    ("scores", RList([RInt(10.I128), RInt(20.I128), RInt(30.I128)])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
