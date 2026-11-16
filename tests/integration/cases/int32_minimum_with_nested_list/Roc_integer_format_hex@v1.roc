Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("minimum", RInt(-0x80000000.I128)),
    ("neighbor", RInt(-0x7fffffff.I128)),
    ("maximum", RInt(0x7fffffff.I128)),
    ("nested", RList([RInt(-0x80000000.I128)])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
