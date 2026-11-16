Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
    RSet(List(Val)),
]

my_data : Val
my_data = RDict([
    ("a", RList([])),
    ("b", RSet([RInt(1.I128), RInt(2.I128)])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
