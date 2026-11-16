Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("plain", RList([RInt(1.I128), RInt(2.I128)])),
    ("with-dash", RStr("a\nb")),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
