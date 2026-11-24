Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("lint", RList([RInt(2.I128), RList([])])),
    ("test", RList([RInt(5.I128), RList([RStr("compile")])])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
