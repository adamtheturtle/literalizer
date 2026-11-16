Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

string_map : Val
string_map = RDict([
    ("k", RStr("s")),
])
my_data : Val
my_data = RList([
    string_map,
    RDict([("k", RInt(1.I128))]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
