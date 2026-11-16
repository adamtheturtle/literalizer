Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("below", RInt(-0o20000000001.I128)),
    ("minimum", RInt(-0o20000000000.I128)),
    ("above", RInt(-0o17777777777.I128)),
    ("nested", RList([RInt(0o0.I128)])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
