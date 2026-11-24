Val := [
    RInt(I128),
]

my_data : Val
my_data = RInt(0x2a.I128)

main! = |_args| {
    _ = my_data
    Ok({})
}
