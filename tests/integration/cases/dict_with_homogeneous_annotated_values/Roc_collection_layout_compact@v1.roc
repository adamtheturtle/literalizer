Val := [
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("a", RList([])),
    ("b", RList([])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
