Val := [
    RStr(Str),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    # before line
    ("value", RStr("left\tright")),  # inline line
    # after line
])

main! = |_args| {
    _ = my_data
    Ok({})
}
