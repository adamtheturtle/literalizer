Val := [
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("mixed", RList([RList([RStr("09:30:00")]), RList([])])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
