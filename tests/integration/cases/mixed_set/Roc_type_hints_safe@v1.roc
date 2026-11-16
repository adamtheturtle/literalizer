Val := [
    RBool(Bool),
    RInt(I128),
    RStr(Str),
    RSet(List(Val)),
]

my_data : Val
my_data = RSet([
    RBool(Bool.True),
    RInt(42.I128),
    RStr("apple"),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
