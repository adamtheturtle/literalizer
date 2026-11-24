Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("left", RList([RInt(1.I128), RStr("one")])),
    ("right", RList([RInt(2.I128), RStr("two")])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
