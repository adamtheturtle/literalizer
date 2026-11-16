Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("alpha", RList([RInt(2.I128), RList([])])),
    ("beta", RList([RInt(5.I128), RList([RStr("x")])])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
