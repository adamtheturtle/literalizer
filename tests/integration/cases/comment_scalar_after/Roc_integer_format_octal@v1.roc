Val := [
    RInt(I128),
]

my_data : Val
my_data = RInt(0o52.I128)
# after

main! = |_args| {
    _ = my_data
    Ok({})
}
