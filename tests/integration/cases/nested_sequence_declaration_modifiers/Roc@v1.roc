Val := [
    RNull,
    RBool(Bool),
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RList([]),
    RList([RInt(1.I128)]),
    RList([RInt(1.I128), RInt(2.I128)]),
    RList([RInt(1.I128), RStr("x"), RBool(Bool.True), RNull]),
    RList([RInt(1.I128), RInt(2.I128), RInt(3.I128), RInt(4.I128), RInt(5.I128), RInt(6.I128), RInt(7.I128), RInt(8.I128)]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
