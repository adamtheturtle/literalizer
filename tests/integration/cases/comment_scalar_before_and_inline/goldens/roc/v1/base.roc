Val := [
    RStr(Str),
]

my_data : Val
my_data = # before
RStr("plain")  # inline

main! = |_args| {
    _ = my_data
    Ok({})
}
