Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("minimum", RInt(-2147483648.I128)),
    ("below", RInt(-3000000000.I128)),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
