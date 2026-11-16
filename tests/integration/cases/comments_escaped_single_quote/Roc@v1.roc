Val := [
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("key", RStr("it's here")),  # a comment
])

main! = |_args| {
    _ = my_data
    Ok({})
}
