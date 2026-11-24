Val := [
    RStr(Str),
]

my_data : Val
my_data = RStr("2024-01-15T18:00:00+05:00")

main! = |_args| {
    _ = my_data
    Ok({})
}
