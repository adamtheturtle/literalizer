Val := [
    RStr(Str),
    RList(List(Val)),
    RSet(List(Val)),
]

my_data : Val
my_data = RList([
    RSet([RStr("a"), RStr("b")]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
