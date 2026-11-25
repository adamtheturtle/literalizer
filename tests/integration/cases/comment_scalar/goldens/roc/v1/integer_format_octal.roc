Val := [
    RInt(I128),
]

my_data : Val
my_data = # note
RInt(0o52.I128)

main! = |_args| {
    _ = my_data
    Ok({})
}
