Val := [
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("v", RStr("a\u(feff)b")),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
