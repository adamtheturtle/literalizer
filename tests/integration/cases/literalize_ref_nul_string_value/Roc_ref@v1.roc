Val := [
    RStr(Str),
    RDict(List((Str, Val))),
]

shared : Val
shared = RStr("a\u(0000)b")
my_data : Val
my_data = RDict([
    ("value", shared),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
