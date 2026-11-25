Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("__proto__", RDict([("x", RInt(1.I128))])),
    ("ordinary", RInt(2.I128)),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
