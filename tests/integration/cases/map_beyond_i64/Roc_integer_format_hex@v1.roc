Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("a", RInt(0x7fffffffffffffff.I128)),
    ("b", RInt(0x8000000000000000.I128)),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
