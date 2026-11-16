Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("single_map", RList([RDict([])])),
    ("single_list", RList([RList([RInt(1.I128)])])),
    ("single_deep", RList([RList([RList([RInt(2.I128)])])])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
