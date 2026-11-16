Val := [
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RList([
    RDict([("", RStr("external_value"))]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
