Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("groups", RList([
        RList([
            RDict([
                ("id", RInt(1.I128)),
            ]),
        ]),
        RList([
            RDict([
                ("id", RInt(2.I128)),
            ]),
        ]),
    ])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
