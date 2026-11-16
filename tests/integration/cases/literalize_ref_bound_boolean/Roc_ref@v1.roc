Val := [
    RBool(Bool),
]

ref_flag : Val
ref_flag = RBool(Bool.True)
my_data : Val
my_data = ref_flag

main! = |_args| {
    _ = my_data
    Ok({})
}
