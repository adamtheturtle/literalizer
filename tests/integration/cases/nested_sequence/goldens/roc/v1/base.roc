Val := [
    RNull,
    RBool(Bool),
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RBool(Bool.True),
    RStr("hi"),
    RList([RInt(1.I128), RInt(2.I128)]),
    RNull,
])

main! = |_args| {
    _ = my_data
    Ok({})
}
