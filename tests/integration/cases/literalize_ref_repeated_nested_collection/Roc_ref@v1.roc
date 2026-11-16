Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

shared : Val
shared = RList([
    RList([RInt(1.I128), RInt(2.I128)]),
    RDict([("value", RInt(1.I128))]),
])
my_data : Val
my_data = RList([
    shared,
    shared,
])

main! = |_args| {
    _ = my_data
    Ok({})
}
