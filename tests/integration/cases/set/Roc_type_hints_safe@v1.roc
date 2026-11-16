Val := [
    RStr(Str),
    RSet(List(Val)),
]

my_data : Val
my_data = RSet([
    RStr("apple"),
    RStr("banana"),
    RStr("cherry"),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
