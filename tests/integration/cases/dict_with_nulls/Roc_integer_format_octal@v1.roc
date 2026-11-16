Val := [
    RNull,
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("name", RStr("Alice")),
    ("score", RNull),
    ("age", RInt(0o36.I128)),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
