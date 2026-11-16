Val := [
    RBool(Bool),
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("h", RList([RInt(1.I128), RStr("a"), RList([RInt(2.I128), RStr("b")]), RDict([("k", RList([RBool(Bool.True)]))])])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
