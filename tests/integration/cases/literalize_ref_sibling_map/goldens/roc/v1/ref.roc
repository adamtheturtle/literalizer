Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

sibling_map : Val
sibling_map = RDict([
    ("k", RInt(2.I128)),
])
my_data : Val
my_data = RList([
    RDict([("k", RInt(1.I128))]),
    sibling_map,
])

main! = |_args| {
    _ = my_data
    Ok({})
}
