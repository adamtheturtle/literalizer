Val := [
    RBool(Bool),
    RInt(I128),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("name", RStr("Ada")),
    ("active", RBool(Bool.True)),
    ("scores", RList([RInt(1.I128), RInt(2.I128), RInt(3.I128)])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
