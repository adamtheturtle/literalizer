Val := [
    RBool(Bool),
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("keep", RBool(Bool.True)),
    ("skip", RInt(0.I128)),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
