Val := [
    RBool(Bool),
    RInt(I128),
    RFloat(F64),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("name", RStr("Alice")),
    ("age", RInt(30.I128)),
    ("active", RBool(Bool.True)),
    ("score", RFloat(4.5.F64)),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
