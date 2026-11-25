Val := [
    RStr(Str),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RStr("price $10"),
    RStr("$HOME"),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
