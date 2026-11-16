Val := [
    RNull,
    RInt(I128),
    RList(List(Val)),
]

my_value : Val
my_value = RNull
my_data : Val
my_data = my_value

main! = |_args| {
    _ = my_data
    Ok({})
}
