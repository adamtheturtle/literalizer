Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("a", RInt(0x1.I128)),
    ("b", RInt(0x10000000000.I128)),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
