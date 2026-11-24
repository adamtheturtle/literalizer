Val := [
    RBool(Bool),
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("collection", RStr("alpha")),
    ("featured_entry", RDict([("id", RInt(100.I128)), ("label", RStr("first entry")), ("enabled", RBool(Bool.False)), ("related_ids", RList([RInt(102.I128), RInt(103.I128)]))])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
