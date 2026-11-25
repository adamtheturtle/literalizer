Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("text", RStr("Record0(")),
    ("number", RInt(0b1.I128)),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
