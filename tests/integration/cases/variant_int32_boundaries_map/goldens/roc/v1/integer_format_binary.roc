Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("below", RInt(-0b10000000000000000000000000000001.I128)),
    ("minimum", RInt(-0b10000000000000000000000000000000.I128)),
    ("above", RInt(-0b1111111111111111111111111111111.I128)),
    ("nested", RList([RInt(0b0.I128)])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
