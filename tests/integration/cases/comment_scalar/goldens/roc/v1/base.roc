Val := [
    RInt(I128),
]

my_data : Val
my_data = # note
RInt(42.I128)

main! = |_args| {
    _ = my_data
    Ok({})
}
