Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("main", RDict([("x", RInt(1.I128)), ("y", RStr("s"))])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
