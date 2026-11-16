Val := [
    RStr(Str),
]

my_data : Val
my_data = # coding: ascii
RStr("café")

main! = |_args| {
    _ = my_data
    Ok({})
}
