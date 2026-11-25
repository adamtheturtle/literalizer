Val := [
    RInt(I128),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RInt(0xde0b6b3a763ffff.I128),
    RInt(-0xde0b6b3a763ffff.I128),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
