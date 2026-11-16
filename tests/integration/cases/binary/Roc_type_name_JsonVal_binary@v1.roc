JsonVal := [
    RStr(Str),
    RList(List(JsonVal)),
]

my_data : JsonVal
my_data = RList([
    RStr("48656c6c6f"),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
