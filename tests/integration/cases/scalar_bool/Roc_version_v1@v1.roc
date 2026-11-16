Val := [
    RBool(Bool),
]

my_data : Val
my_data = RBool(Bool.True)

main! = |_args| {
    _ = my_data
    Ok({})
}
