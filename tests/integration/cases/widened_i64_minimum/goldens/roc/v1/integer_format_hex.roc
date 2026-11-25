Val := [
    RInt(I128),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RInt(-0x8000000000000000.I128),
    RInt(0x5.I128),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
