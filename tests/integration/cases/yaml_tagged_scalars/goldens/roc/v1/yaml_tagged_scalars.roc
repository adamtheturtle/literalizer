Val := [
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("explicit_string", RStr("5")),
    ("six", RStr("explicitly tagged key")),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
