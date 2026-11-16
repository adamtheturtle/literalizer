Val := [
    RStr(Str),
]

my_data : Val
my_data = RStr("1901-12-13T20:45:51")

main! = |_args| {
    _ = my_data
    Ok({})
}
