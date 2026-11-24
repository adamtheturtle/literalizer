Val := [
    RInt(I128),
]

my_data : Val
my_data = RInt(1705323600.I128)

main! = |_args| {
    _ = my_data
    Ok({})
}
