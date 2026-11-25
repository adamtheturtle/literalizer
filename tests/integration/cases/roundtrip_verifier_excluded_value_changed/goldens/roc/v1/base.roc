Val := [
    RBool(Bool),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("keep", RBool(Bool.True)),
    ("skip", RBool(Bool.False)),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
