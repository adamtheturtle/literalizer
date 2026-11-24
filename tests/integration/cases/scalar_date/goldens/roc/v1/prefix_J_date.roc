Val := [
    JStr(Str),
]

my_data : Val
my_data = JStr("2024-01-15")

main! = |_args| {
    _ = my_data
    Ok({})
}
