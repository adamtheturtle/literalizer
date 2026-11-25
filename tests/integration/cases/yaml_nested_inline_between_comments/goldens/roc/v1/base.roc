Val := [
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RList([RInt(2.I128), RStr("hello")]),  # trailing note
    # next element
    RList([RInt(3.I128), RStr("world")]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
