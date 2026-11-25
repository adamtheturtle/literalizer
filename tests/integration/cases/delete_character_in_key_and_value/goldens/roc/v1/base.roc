Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("v", RStr("a\u(007f)b")),
    ("a\u(007f)b", RInt(1.I128)),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
