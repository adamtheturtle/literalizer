Val := [
    RNull,
    RBool(Bool),
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RInt(0b1.I128),
    RStr("hello"),
    RBool(Bool.True),
    RNull,
])

main! = |_args| {
    _ = my_data
    Ok({})
}
