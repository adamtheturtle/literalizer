Val := [
    RNull,
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("host", RStr("localhost")),
    ("port", RNull),  # not configured yet
])

main! = |_args| {
    _ = my_data
    Ok({})
}
