Val := [
    RBool(Bool),
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
    RSet(List(Val)),
]

my_data : Val
my_data = RDict([
    ("name", RStr("Alice")),
    ("tags", RSet([
        RBool(Bool.True),
        RInt(42.I128),
        RStr("apple"),
    ])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
