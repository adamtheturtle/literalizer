Val := [
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("08", RStr("value")),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
