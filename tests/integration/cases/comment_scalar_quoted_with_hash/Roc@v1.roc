Val := [
    RStr(Str),
]

my_data : Val
my_data = RStr("hello # world")  # note

main! = |_args| {
    _ = my_data
    Ok({})
}
