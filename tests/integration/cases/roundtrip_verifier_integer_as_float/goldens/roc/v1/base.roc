Val := [
    RFloat(F64),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("value", RFloat(1.0.F64)),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
