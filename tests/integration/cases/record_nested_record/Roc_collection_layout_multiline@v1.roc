Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("id", RInt(1.I128)),
    ("owner", RDict([
        ("name", RStr("Alice")),
        ("age", RInt(30.I128)),
    ])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
