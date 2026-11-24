Val := [
    RInt(I128),
    RList(List(Val)),
]

ref_data : Val
ref_data = RList([
    RInt(1.I128),
    RInt(2.I128),
])
my_data : Val
my_data = ref_data

main! = |_args| {
    _ = my_data
    Ok({})
}
