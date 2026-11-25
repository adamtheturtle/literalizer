Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("scores", RList([RInt(10.I128), RInt(20.I128), RInt(30.I128)])),
    ("args", RList([RInt(1.I128), RStr("email"), RStr("a@gmail.com"), RInt(100.I128)])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
