Val := [
    RStr(Str),
]

my_data : Val
my_data = RStr("a\u(0085)b\u(2028)c\u(2029)d\r\u(2028)e")

main! = |_args| {
    _ = my_data
    Ok({})
}
