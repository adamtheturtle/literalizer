Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("minimum", RInt(-0b10000000000000000000000000000000.I128)),
    ("neighbor", RInt(-0b1111111111111111111111111111111.I128)),
    ("maximum", RInt(0b1111111111111111111111111111111.I128)),
    ("nested", RList([RInt(-0b10000000000000000000000000000000.I128)])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
