Val := [
    RInt(I128),
    RFloat(F64),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RList([
    RDict([
        ("x", RInt(1.I128)),
        ("y", RFloat(2.5.F64)),
    ]),
    RDict([
        ("x", RInt(3.I128)),
        ("y", RFloat(4.0.F64)),
    ]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
