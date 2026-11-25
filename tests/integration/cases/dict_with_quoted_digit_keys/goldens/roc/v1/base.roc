Val := [
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("0a", RStr("first")),
    ("1b", RStr("second")),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
