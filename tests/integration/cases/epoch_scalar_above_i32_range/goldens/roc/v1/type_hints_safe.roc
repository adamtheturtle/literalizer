Val := [
    RStr(Str),
]

my_data : Val
my_data = RStr("2099-06-15T08:30:00")

main! = |_args| {
    _ = my_data
    Ok({})
}
