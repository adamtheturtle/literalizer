Val := [
    RStr(Str),
]

my_data : Val
my_data = RStr("\u(007f)0\u(0080)a\u(009f)F")

main! = |_args| {
    _ = my_data
    Ok({})
}
