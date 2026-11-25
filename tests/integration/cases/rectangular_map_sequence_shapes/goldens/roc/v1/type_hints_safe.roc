Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("a", RList([RDict([("item", RList([RInt(1.I128)]))])])),
    ("b", RList([RDict([("item", RList([RInt(2.I128)]))])])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
