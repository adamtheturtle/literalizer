Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    # Configuration
    ("name", RStr("app")),
    # Port setting
    ("port", RInt(3000.I128)),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
