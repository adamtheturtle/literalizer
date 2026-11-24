Val := [
    RBool(Bool),
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("value", RList([RBool(Bool.True), RBool(Bool.False), RInt(0.I128), RInt(1.I128)])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
