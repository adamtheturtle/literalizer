Val := [
    RStr(Str),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RStr("prefix \${HOME} suffix"),
    RStr("\${interpolated}"),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
