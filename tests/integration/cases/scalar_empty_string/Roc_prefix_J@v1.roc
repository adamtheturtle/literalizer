Val := [
    JStr(Str),
]

my_data : Val
my_data = JStr("")

main! = |_args| {
    _ = my_data
    Ok({})
}
