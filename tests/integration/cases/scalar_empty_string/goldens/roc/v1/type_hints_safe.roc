Val := [
    RStr(Str),
]

my_data : Val
my_data = RStr("")

main! = |_args| {
    _ = my_data
    Ok({})
}
