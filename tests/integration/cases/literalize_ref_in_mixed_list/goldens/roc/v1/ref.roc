Val := [
    RInt(I128),
    RList(List(Val)),
]

ref_x : Val
ref_x = RInt(3.I128)
my_data : Val
my_data = RList([
    ref_x,
    RInt(1.I128),
    RInt(2.I128),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
