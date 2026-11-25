Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("lint", RList([RInt(2.I128), RList([RInt(1.I128)])])),
    ("test", RList([RInt(5.I128), RList([RInt(7.I128)])])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
