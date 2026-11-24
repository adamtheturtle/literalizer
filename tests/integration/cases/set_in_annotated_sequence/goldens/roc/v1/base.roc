Val := [
    RInt(I128),
    RList(List(Val)),
    RSet(List(Val)),
]

my_data : Val
my_data = RList([
    RSet([]),
    RSet([RInt(1.I128), RInt(2.I128)]),
    RList([]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
