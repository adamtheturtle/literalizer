Val := [
    RNull,
    RBool(Bool),
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("name", RStr("Alice")),
    ("age", RInt(30.I128)),
    ("active", RBool(Bool.True)),
    ("score", RNull)
])

main! = |_args| {
    _ = my_data
    Ok({})
}
