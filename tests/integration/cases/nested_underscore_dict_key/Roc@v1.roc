Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("outer", RList([RDict([("_", RInt(1.I128))])])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
