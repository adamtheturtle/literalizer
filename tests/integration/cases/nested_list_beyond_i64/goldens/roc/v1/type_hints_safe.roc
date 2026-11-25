Val := [
    RInt(I128),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RList([RInt(1.I128)]),
    RList([RInt(1180591620717411303424.I128)]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
