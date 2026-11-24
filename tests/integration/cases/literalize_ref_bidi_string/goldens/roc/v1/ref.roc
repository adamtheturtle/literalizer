Val := [
    RStr(Str),
    RDict(List((Str, Val))),
]

text : Val
text = RStr("a\u(202a)b")
my_data : Val
my_data = RDict([
    ("value", text),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
