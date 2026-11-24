Val := [
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("my-key", RStr("value1")),
    ("another-key", RStr("value2")),
    ("normal_key", RStr("value3")),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
