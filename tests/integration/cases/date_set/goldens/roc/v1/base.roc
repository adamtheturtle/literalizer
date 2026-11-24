Val := [
    RStr(Str),
    RSet(List(Val)),
]

my_data : Val
my_data = RSet([
    RStr("2024-01-15"),
    RStr("2024-06-01"),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
