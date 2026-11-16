Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("first", RList([RList([RInt(1.I128), RStr("value")]), RList([])])),
    ("second", RList([RList([]), RList([RInt(2.I128), RStr("other")])])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
