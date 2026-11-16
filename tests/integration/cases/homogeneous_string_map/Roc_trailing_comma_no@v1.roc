Val := [
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("a", RStr("x")),
    ("b", RStr("y"))
])

main! = |_args| {
    _ = my_data
    Ok({})
}
