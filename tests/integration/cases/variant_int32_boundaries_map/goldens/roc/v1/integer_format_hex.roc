Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("below", RInt(-0x80000001.I128)),
    ("minimum", RInt(-0x80000000.I128)),
    ("above", RInt(-0x7fffffff.I128)),
    ("nested", RList([RInt(0x0.I128)])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
