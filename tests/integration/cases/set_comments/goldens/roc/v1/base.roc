Val := [
    RStr(Str),
    RSet(List(Val)),
]

my_data : Val
my_data = RSet([
    RStr("apple"),  # inline comment
    # before banana
    RStr("banana"),
    # trailing
])

main! = |_args| {
    _ = my_data
    Ok({})
}
