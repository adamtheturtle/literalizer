Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    # About the first dotted key.
    # About the second dotted key.
    ("dotted", RDict([
        ("first", RInt(1.I128)),
        ("second", RInt(2.I128)),
    ])),
    ("plain", RInt(3.I128)),  # About the plain key.
    # Before the first entry.
    # Before the second entry.
    ("entries", RList([
        RDict([
            ("name", RStr("one")),
        ]),
        RDict([
            ("name", RStr("two")),
        ]),
    ])),
    # Inside the table.
    ("table", RDict([
        ("inner", RInt(4.I128)),
    ])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
