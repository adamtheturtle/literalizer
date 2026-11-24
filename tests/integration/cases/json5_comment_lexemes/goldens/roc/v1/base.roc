Val := [
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    # heading
    ("a", RStr("single ' // data")),
    ("b", RStr("linecontinuation")),
    ("c", RStr("\\")),  # actual comment
    ("d", RStr("\u(2028)\u(2029)")),  # final comment
])

main! = |_args| {
    _ = my_data
    Ok({})
}
