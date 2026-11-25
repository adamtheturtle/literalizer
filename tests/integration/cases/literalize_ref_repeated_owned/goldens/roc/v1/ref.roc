Val := [
    RInt(I128),
    RList(List(Val)),
]

shared : Val
shared = RList([
    RInt(1.I128),
    RInt(2.I128),
])
my_data : Val
my_data = RList([
    shared,
    shared,
])

main! = |_args| {
    _ = my_data
    Ok({})
}
