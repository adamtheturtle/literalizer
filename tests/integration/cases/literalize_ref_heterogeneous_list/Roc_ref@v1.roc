Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
]

one : Val
one = RInt(1.I128)
two : Val
two = RStr("s")
my_data : Val
my_data = RList([
    one,
    two,
])

main! = |_args| {
    _ = my_data
    Ok({})
}
