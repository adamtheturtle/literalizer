Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("minimum", RInt(-0o20000000000.I128)),
    ("below", RInt(-0o26264057000.I128)),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
