Val := [
    RBool(Bool),
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RInt(1.I128),
    RStr("hello"),
    RBool(Bool.True),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
