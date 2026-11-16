Val := [
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("del", RStr("a\u(007f)b")),
    ("nel", RStr("a\u(0085)b")),
    ("c1", RStr("a\u(009f)b")),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
