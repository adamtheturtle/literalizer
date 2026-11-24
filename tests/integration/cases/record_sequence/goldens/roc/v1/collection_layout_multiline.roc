Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RList([
    RDict([
        ("id", RInt(1.I128)),
        ("label", RStr("first")),
        ("tags", RList([])),
    ]),
    RDict([
        ("id", RInt(2.I128)),
        ("label", RStr("second")),
        ("tags", RList([])),
    ]),
    RDict([
        ("id", RInt(3.I128)),
        ("label", RStr("third")),
        ("tags", RList([])),
    ]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
