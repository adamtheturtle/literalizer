Val := [
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("v", RStr("a\u(202a)\u(202b)\u(202c)\u(202d)\u(202e)\u(2066)\u(2067)\u(2068)\u(2069)b")),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
