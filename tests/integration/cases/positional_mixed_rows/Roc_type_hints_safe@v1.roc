Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RList([RList([RInt(1.I128), RStr("value")]), RList([RInt(1.I128), RInt(2.I128)]), RList([])]),
    RList([RList([]), RList([]), RList([RInt(3.I128), RInt(4.I128)])]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
