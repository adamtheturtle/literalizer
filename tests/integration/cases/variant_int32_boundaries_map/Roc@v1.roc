Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("below", RInt(-2147483649.I128)),
    ("minimum", RInt(-2147483648.I128)),
    ("above", RInt(-2147483647.I128)),
    ("nested", RList([RInt(0.I128)])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
