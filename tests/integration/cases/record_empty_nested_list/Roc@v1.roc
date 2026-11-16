Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("a", RList([RList([RInt(1.I128), RInt(2.I128)]), RList([RInt(3.I128)])])),
    ("b", RList([RList([]), RList([RInt(1.I128)])])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
