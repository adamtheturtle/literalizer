Val := [
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("text", RStr("a\"//b")),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
