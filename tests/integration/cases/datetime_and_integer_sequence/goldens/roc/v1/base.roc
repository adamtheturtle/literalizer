Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RStr("2000-01-01T01:02:03"),
    RInt(1.I128),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
