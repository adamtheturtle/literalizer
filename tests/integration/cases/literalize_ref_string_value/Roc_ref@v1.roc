Val := [
    RStr(Str),
    RDict(List((Str, Val))),
]

shared : Val
shared = RStr("s")
my_data : Val
my_data = RDict([
    ("value", shared),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
