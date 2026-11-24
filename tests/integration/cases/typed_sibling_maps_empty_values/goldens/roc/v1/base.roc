Val := [
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RList([
    RDict([("m", RDict([]))]),
    RDict([("m", RDict([]))]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
