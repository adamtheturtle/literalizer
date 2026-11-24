Val := [
    RNull,
]

value : Val
value = RNull
my_data : Val
my_data = value

main! = |_args| {
    _ = my_data
    Ok({})
}
