Val := [
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("description", RStr("# not a comment\n")),
    ("name", RStr("foo")),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
