Val := [
    RBool(Bool),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RBool(Bool.True),
    RBool(Bool.False),
    RBool(Bool.True),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
