Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("a", RInt(9223372036854775807.I128)),
    ("b", RInt(9223372036854775808.I128)),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
