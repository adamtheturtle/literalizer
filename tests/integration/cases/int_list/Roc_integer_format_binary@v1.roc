Val := [
    RInt(I128),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RInt(0b1.I128),
    RInt(0b10.I128),
    RInt(0b11.I128),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
