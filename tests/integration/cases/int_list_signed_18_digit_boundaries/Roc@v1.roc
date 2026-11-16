Val := [
    RInt(I128),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RInt(999999999999999999.I128),
    RInt(-999999999999999999.I128),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
