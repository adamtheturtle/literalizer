Val := [
    RInt(I128),
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("host", RStr("it's here")),  # a comment
    ("port", RInt(80.I128)),  # another
])

main! = |_args| {
    _ = my_data
    Ok({})
}
