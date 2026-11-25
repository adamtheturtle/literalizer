Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("a", RInt(1.I128)),
    ("b", RStr("x")),
    ("e", RList([RInt(1.I128), RInt(2.I128)])),
    ("f", RDict([("g", RStr("h"))])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
