Val := [
    RInt(I128),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RList([
        RInt(1.I128),
        RInt(2.I128),
    ]),
    RList([]),
    RList([
        RInt(3.I128),
        RInt(4.I128),
    ]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
