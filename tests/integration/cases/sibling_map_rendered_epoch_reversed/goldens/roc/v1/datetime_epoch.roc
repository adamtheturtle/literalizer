Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("b", RDict([("k", RInt(1.I128))])),
    ("a", RDict([("k", RInt(2208988800.I128))])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
