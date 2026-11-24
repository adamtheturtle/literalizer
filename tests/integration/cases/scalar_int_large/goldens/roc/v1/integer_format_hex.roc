Val := [
    RInt(I128),
]

my_data : Val
my_data = RInt(0x80000000.I128)

main! = |_args| {
    _ = my_data
    Ok({})
}
