Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("first", RDict([("items", RList([RInt(1.I128), RDict([("value", RInt(2.I128))])]))])),
    ("second", RDict([("items", RList([RInt(1.I128), RDict([("value", RStr("s"))])]))])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
