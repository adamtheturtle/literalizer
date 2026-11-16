Val := [
    RStr(Str),
]

my_data : Val
my_data = RStr("2024-01-15T00:00:00")

main! = |_args| {
    _ = my_data
    Ok({})
}
