Val := [
    RStr(Str),
]

my_data : Val
my_data = RStr("2020-06-15T12:00:00+23:59")

main! = |_args| {
    _ = my_data
    Ok({})
}
