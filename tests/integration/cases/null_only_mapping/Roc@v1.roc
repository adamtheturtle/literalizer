Val := [
    RNull,
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("value", RNull),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
