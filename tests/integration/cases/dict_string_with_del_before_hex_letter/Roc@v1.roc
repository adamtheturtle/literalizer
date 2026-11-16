Val := [
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("value", RStr("del\u(007f)d")),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
