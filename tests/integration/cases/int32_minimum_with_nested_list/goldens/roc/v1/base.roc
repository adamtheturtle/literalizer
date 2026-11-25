Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("minimum", RInt(-2147483648.I128)),
    ("neighbor", RInt(-2147483647.I128)),
    ("maximum", RInt(2147483647.I128)),
    ("nested", RList([RInt(-2147483648.I128)])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
