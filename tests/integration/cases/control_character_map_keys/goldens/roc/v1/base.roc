Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("", RInt(1.I128)),
    ("a\u(0001)b", RInt(2.I128)),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
