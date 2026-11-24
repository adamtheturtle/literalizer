Val := [
    RBool(Bool),
    RInt(I128),
    RFloat(F64),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("below", RList([RList([RList([RList([RList([RList([RList([RList([RInt(1.I128)])])])])])])])])),
    ("boundary", RList([RList([RList([RList([RList([RList([RList([RList([RList([RInt(2.I128)])])])])])])])])])),
    ("multiple", RList([RList([RList([RList([RList([RList([RList([RList([RList([RList([RList([RList([RList([RList([RList([RList([RList([RInt(3.I128)])])])])])])])])])])])])])])])])])),
    ("text", RList([RList([RList([RList([RList([RList([RList([RList([RList([RStr("value")])])])])])])])])])),
    ("boolean", RList([RList([RList([RList([RList([RList([RList([RList([RList([RBool(Bool.True)])])])])])])])])])),
    ("float", RList([RList([RList([RList([RList([RList([RList([RList([RList([RFloat(1.5.F64)])])])])])])])])])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
