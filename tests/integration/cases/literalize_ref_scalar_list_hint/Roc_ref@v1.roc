Val := [
    RInt(I128),
    RList(List(Val)),
]

ref_data : Val
ref_data = RInt(1.I128)
my_data : Val
my_data = ref_data

main! = |_args| {
    _ = my_data
    Ok({})
}
