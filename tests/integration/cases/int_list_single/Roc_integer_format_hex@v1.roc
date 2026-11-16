Val := [
    RInt(I128),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RInt(0x1.I128),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
