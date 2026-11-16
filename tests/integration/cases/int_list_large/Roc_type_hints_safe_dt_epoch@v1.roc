Val := [
    RInt(I128),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RInt(1000000.I128),
    RInt(-1234.I128),
    RInt(255.I128),
    RInt(-10.I128),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
