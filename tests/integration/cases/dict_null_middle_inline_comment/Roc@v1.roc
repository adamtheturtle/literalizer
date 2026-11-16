Val := [
    RNull,
    RBool(Bool),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("server", RDict([
        ("host", RStr("localhost")),
        ("port", RNull),  # not configured yet
        ("debug", RBool(Bool.True)),
    ])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
