Val := [
    RInt(I128),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RInt(0o3641100.I128),
    RInt(-0o2322.I128),
    RInt(0o377.I128),
    RInt(-0o12.I128),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
