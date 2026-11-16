Val := [
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("comma_hash", RStr("a,#b")),
    ("comma_space_hash", RStr("trail, # comment")),
    ("escaped_quote", RStr("quote \" and , #")),
    ("next_line", RStr("x\u(0085)y")),
    ("line_separator", RStr("x\u(2028)y")),
    ("paragraph_separator", RStr("x\u(2029)y")),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
