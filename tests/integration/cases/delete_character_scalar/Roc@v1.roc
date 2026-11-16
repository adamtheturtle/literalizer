Val := [
    RStr(Str),
]

my_data : Val
my_data = RStr("\u(007f)")

main! = |_args| {
    _ = my_data
    Ok({})
}
