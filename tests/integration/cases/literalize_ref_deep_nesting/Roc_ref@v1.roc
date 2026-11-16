Val := [
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

deep : Val
deep = RList([
    RList([
        RStr("one"),
        RStr("two"),
    ]),
    RList([
        RStr("three"),
        RStr("four"),
    ]),
])
my_data : Val
my_data = RDict([
    ("a", RDict([
        ("b", RDict([
            ("c", deep),
        ])),
    ])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
