Val := [
    RInt(I128),
    RFloat(F64),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("_", RList([RInt(1.I128), RFloat(2.5.F64), RInt(3.I128)])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
