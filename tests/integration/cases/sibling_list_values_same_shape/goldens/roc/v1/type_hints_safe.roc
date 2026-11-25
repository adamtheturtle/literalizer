Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("test", RList([RInt(5.I128), RList([RStr("compile"), RStr("test")])])),
    ("package", RList([RInt(7.I128), RList([RStr("link"), RStr("test")])])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
