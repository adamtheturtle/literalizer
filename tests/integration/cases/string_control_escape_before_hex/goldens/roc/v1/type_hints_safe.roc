Val := [
    RStr(Str),
]

my_data : Val
my_data = RStr("a\u(0007)face")

main! = |_args| {
    _ = my_data
    Ok({})
}
