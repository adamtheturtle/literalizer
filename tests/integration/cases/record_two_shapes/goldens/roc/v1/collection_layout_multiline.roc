Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("metrics", RDict([
        ("count", RInt(100.I128)),
        ("rate", RInt(50.I128)),
    ])),
    ("flags", RDict([
        ("retries", RInt(3.I128)),
        ("timeout", RInt(30.I128)),
    ])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
