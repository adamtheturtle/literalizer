Val := [
    RInt(I128),
    RList(List(Val)),
]

existing : Val
existing = RInt(1.I128)
my_data : Val
my_data = RList([
    RInt(0.I128),
    RList([RList([existing])]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
