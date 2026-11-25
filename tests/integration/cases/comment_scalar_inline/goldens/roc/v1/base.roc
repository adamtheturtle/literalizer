Val := [
    RInt(I128),
]

my_data : Val
my_data = RInt(42.I128)  # note

main! = |_args| {
    _ = my_data
    Ok({})
}
