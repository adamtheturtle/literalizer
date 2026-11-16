Val := [
    RInt(I128),
]

my_data : Val
my_data = RInt(-0x80000001.I128)

main! = |_args| {
    _ = my_data
    Ok({})
}
