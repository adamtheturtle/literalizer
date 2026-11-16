Val := [
    RStr(Str),
    RDict(List((Str, Val))),
]

existing : Val
existing = RDict([
    ("_", RStr("_")),
])
my_data : Val
my_data = existing

main! = |_args| {
    _ = my_data
    Ok({})
}
