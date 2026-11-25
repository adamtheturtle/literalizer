Val := [
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("ts", RStr("3000-12-31T23:59:59.999999+00:00")),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
