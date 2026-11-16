Val := [
    RNull,
]

my_data : Val
my_data = RNull  # note

main! = |_args| {
    _ = my_data
    Ok({})
}
