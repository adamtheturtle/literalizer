Val := [
    RNull,
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("a", RNull),
    ("b", RNull),
    # trailing
])

main! = |_args| {
    _ = my_data
    Ok({})
}
