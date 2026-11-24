Val := [
    RStr(Str),
]

source_value : Val
source_value = RStr("\u(fffe)\u(ffff)")
my_data : Val
my_data = source_value

main! = |_args| {
    _ = my_data
    Ok({})
}
