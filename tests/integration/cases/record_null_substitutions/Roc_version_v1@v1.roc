Val := [
    RNull,
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("rows", RList([RDict([("replacement", RNull), ("present", RInt(1.I128))]), RDict([("replacement", RInt(2.I128)), ("present", RInt(3.I128))])])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
