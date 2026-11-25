Val := [
    RBool(Bool),
    RInt(I128),
    RFloat(F64),
    RStr(Str),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RInt(0x2a.I128),
    RFloat(3.14.F64),
    RBool(Bool.True),
    RBool(Bool.False),
    RStr("hello \"world\""),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
