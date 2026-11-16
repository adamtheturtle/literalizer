Val := [
    RStr(Str),
]

my_data : Val
my_data = RStr("\u(0000)x")

main! = |_args| {
    _ = my_data
    Ok({})
}
