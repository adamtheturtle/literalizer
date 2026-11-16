Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("title", RStr("report")),
    ("tags", RList([RStr("draft"), RStr("urgent"), RStr("review")])),
    ("priority", RInt(2.I128)),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
