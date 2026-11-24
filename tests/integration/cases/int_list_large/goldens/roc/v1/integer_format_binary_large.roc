Val := [
    RInt(I128),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RInt(0b11110100001001000000.I128),
    RInt(-0b10011010010.I128),
    RInt(0b11111111.I128),
    RInt(-0b1010.I128),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
