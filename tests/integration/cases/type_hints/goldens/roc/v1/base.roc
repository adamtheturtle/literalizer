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
    ("score", RNull),
    ("joined", RStr("2024-01-15")),
    ("last_login", RStr("2024-01-15T12:30:00+00:00")),
    ("avatar", RStr("48656c6c6f")),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
