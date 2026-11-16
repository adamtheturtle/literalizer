Val := [
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RList([
    RDict([("item", RStr("existing"))]),
    # This comment describes the next item.
    RDict([("item", RStr("next"))]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
