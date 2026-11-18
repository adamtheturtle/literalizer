Val := [
    RStr(Str),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RStr("SGVsbG8="),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
