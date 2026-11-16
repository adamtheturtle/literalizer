Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("minimum", RInt(-0x80000000.I128)),
    ("below", RInt(-0xb2d05e00.I128)),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
