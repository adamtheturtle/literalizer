Val := [
    RNull,
    RBool(Bool),
    RInt(I128),
    RFloat(F64),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RList([
    RDict([("a", RInt(1.I128))]),
    RInt(1.I128),
    RStr("x"),
    RBool(Bool.True),
    RFloat(2.5.F64),
    RNull,
])

main! = |_args| {
    _ = my_data
    Ok({})
}
