Val := [
    RBool(Bool),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RList([RBool(Bool.True), RBool(Bool.False)]),
    RList([RBool(Bool.True), RBool(Bool.True)]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
