Val := [
    RInt(I128),
    RFloat(F64),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("a", RInt(0o1.I128)),
    ("b", RFloat(2.5.F64)),
    ("c", RInt(0o3.I128)),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
