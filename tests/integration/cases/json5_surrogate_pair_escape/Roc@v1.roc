Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("astral", RStr("😀")),
    ("mixed", RStr("a😀b")),
    ("count", RInt(2.I128)),
    ("list", RList([RStr("😀"), RInt(1.I128)])),
    ("nested", RDict([("inner", RStr("😀"))])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
