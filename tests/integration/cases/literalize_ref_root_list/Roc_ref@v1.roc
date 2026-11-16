Val := [
    RInt(I128),
    RList(List(Val)),
]

whole : Val
whole = RList([
    RInt(1.I128),
    RInt(2.I128),
])
my_data : Val
my_data = whole

main! = |_args| {
    _ = my_data
    Ok({})
}
