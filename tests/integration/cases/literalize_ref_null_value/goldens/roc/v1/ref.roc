Val := [
    RNull,
]

my_null : Val
my_null = RNull
my_data : Val
my_data = my_null

main! = |_args| {
    _ = my_data
    Ok({})
}
