Val := [
    RInt(I128),
]

my_int : Val
my_int = RInt(42.I128)
my_data : Val
my_data = my_int

main! = |_args| {
    _ = my_data
    Ok({})
}
