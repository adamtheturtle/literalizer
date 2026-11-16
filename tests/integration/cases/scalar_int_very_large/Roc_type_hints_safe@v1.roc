Val := [
    RInt(I128),
]

my_data : Val
my_data = RInt(9223372036854775808.I128)

main! = |_args| {
    _ = my_data
    Ok({})
}
