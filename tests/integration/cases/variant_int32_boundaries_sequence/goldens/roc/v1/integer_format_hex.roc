Val := [
    RInt(I128),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RInt(-0x80000000.I128),
    RInt(-0x7fffffff.I128),
    RList([RInt(0x0.I128)]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
