Val := [
    RNull,
    RInt(I128),
    RList(List(Val)),
]

my_value : Val
my_value = RList([
    RInt(1.I128),
    RInt(2.I128),
])
my_data : Val
my_data = my_value

main! = |_args| {
    _ = my_data
    Ok({})
}
