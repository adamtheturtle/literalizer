Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("deep", RList([RList([RList([RList([RList([RList([RList([RList([RList([RList([RList([RList([RList([RList([RList([RList([RList([RList([RList([RList([RList([RList([RList([RList([RList([RList([RList([RList([RList([RList([RInt(1.I128)])])])])])])])])])])])])])])])])])])])])])])])])])])])])])])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
