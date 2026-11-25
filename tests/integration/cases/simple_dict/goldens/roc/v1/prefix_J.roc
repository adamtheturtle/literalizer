Val := [
    JNull,
    JBool(Bool),
    JInt(I128),
    JStr(Str),
    JDict(List((Str, Val))),
]

my_data : Val
my_data = JDict([
    ("name", JStr("Alice")),
    ("age", JInt(30.I128)),
    ("active", JBool(Bool.True)),
    ("score", JNull),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
