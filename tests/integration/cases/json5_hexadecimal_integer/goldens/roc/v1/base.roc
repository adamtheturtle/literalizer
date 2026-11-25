Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("lower", RInt(3735928559.I128)),
    ("upper", RInt(31.I128)),
    ("negative", RInt(-16.I128)),
    ("zero", RInt(0.I128)),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
