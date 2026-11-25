Val := [
    RInt(I128),
]

my_data : Val
my_data = RInt(1592136060.I128)

main! = |_args| {
    _ = my_data
    Ok({})
}
