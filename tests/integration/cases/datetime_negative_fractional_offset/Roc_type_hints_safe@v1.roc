Val := [
    RStr(Str),
]

my_data : Val
my_data = RStr("2000-01-01T00:00:00-05:30")

main! = |_args| {
    _ = my_data
    Ok({})
}
