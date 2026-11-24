Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
]

shared : Val
shared = RList([
    RInt(1.I128),
    RStr("x"),
])
my_data : Val
my_data = RList([
    shared,
    shared,
])

main! = |_args| {
    _ = my_data
    Ok({})
}
