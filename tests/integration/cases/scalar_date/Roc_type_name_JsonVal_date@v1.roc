JsonVal := [
    RStr(Str),
]

my_data : JsonVal
my_data = RStr("2024-01-15")

main! = |_args| {
    _ = my_data
    Ok({})
}
