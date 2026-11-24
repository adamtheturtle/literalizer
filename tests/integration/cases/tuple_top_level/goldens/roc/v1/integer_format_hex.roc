Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RInt(0x1.I128),
    RStr("email"),
    RStr("a@gmail.com"),
    RInt(0x64.I128),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
