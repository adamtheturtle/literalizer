Val := [
    RStr(Str),
    RList(List(Val)),
]

my_data : Val
my_data = RList([
    RList([RStr("\nfirst line\n  indented\n\nlast line\n")]),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
