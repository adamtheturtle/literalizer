Val := [
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("double", RStr("a\u(2028)b")),
    ("single", RStr("c\u(2029)d")),
    # A comment, which both separators would end.
    ("both", RStr("e\u(2028)f\u(2029)g")),
    ("continued", RStr("hi")),
    ("escaped backslash", RStr("j\\\u(2028)k")),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
