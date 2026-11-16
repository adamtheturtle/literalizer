Val := [
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("users", RList([
        RDict([
            ("name", RStr("Bob")),
            ("tags", RList([
                RStr("admin"),
                RStr("user"),
            ])),
        ]),
        RDict([
            ("name", RStr("Carol")),
            ("tags", RList([
                RStr("guest"),
            ])),
        ]),
    ])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
