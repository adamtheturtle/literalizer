Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("a", RInt(0o1.I128)),
    ("b", RInt(0o20000000000000.I128)),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
