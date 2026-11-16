Val := [
    RStr(Str),
]

my_data : Val
my_data = RStr("1969-12-31T23:59:59+00:00")

main! = |_args| {
    _ = my_data
    Ok({})
}
