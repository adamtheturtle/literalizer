Val := [
    RNull,
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

actual : Val
actual = RInt(42.I128)
my_data : Val
my_data = RList([
    RDict([("$ref", RInt(1.I128))]),
    RDict([("$ref", RNull)]),
    actual,
])

main! = |_args| {
    _ = my_data
    Ok({})
}
