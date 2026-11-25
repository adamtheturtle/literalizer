Val := [
    RNull,
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    # comment
    ("name", RStr("Alice")),
    ("score", RNull),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
