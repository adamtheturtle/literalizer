Val := [
    RBool(Bool),
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("id", RInt(1.I128)),
    ("label", RStr("She said \"hello\", then waved")),
    ("enabled", RBool(Bool.False)),
    ("related_ids", RList([
        RInt(1.I128),
        RInt(2.I128),
        RInt(3.I128),
    ])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
