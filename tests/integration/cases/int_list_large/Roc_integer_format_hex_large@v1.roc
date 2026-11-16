Val := [
    RInt(I128),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RInt(0xf4240.I128),
    RInt(-0x4d2.I128),
    RInt(0xff.I128),
    RInt(-0xa.I128),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
